"""Validate content and render both the local preview and print job."""

import html
import os
import socket
import textwrap

from .templates import TEMPLATES


class LabelError(ValueError):
    """User input does not fit a template."""


def prepare(payload):
    """Return a template and bounded lines from untrusted request content."""
    if not isinstance(payload, dict):
        raise LabelError("Expected a JSON object.")
    template_id = payload.get("template")
    template = TEMPLATES.get(template_id) if isinstance(template_id, str) else None
    if template is None:
        raise LabelError("Choose a valid template.")
    values = payload.get("values")
    if not isinstance(values, dict):
        raise LabelError("Expected template values.")
    copies = payload.get("copies", 1)
    if type(copies) is not int or not 1 <= copies <= 10:
        raise LabelError("Copies must be between 1 and 10.")
    if set(values) - {f["id"] for f in template["fields"]}:
        raise LabelError("The template contains an unknown field.")
    result = {}
    for field in template["fields"]:
        value = values.get(field["id"], "")
        if not isinstance(value, str):
            raise LabelError(f"{field['label']} must be text.")
        if any(ord(char) < 32 or ord(char) > 126 for char in value):
            raise LabelError(f"{field['label']} supports printable ASCII characters only.")
        value = " ".join(value.split())
        if len(value) > field["limit"]:
            raise LabelError(f"{field['label']} is too long ({field['limit']} characters maximum).")
        if field["required"] and not value:
            raise LabelError(f"{field['label']} is required.")
        chars = max(1, int(field["width"] / (field["font"] * 0.64)))
        wrapped = textwrap.wrap(value, width=chars, break_long_words=True, break_on_hyphens=False)
        if len(wrapped) > field["lines"]:
            raise LabelError(f"{field['label']} will not fit. Shorten it.")
        result[field["id"]] = wrapped
    return template, result, copies


def render_zpl(template, values, copies=1, dpi=203):
    """Build a bounded ZPL job at either supported ZD621 resolution."""
    if dpi not in (203, 300):
        raise ValueError("PRINTER_DPI must be 203 or 300.")
    dot = lambda number: round(number * dpi / 203)
    commands = ["^XA", "^CI28", f"^PW{dot(template['width'])}",
                f"^LL{dot(template['height'])}", "^LH0,0", f"^PQ{copies}",
                f"^FO{dot(24)},0^GB{dot(template['width']-48)},0,{dot(4)}^FS"]
    for field in template["fields"]:
        if field["checkbox"]:
            commands.append(f"^FO{dot(40)},{dot(field['y']+4)}^GB{dot(27)},{dot(27)},{dot(3)}^FS")
        for index, line in enumerate(values[field["id"]]):
            x, y, size = dot(field["x"]), dot(field["y"] + index*field["font"]*1.15), dot(field["font"])
            encoded = "".join(f"_{ord(char):02X}" if char in "^~_" else char for char in line)
            commands.append(f"^FO{x},{y}^A0N,{size},{size}^FH^FD{encoded}^FS")
    return "\n".join([*commands, "^XZ", ""])


def render_svg(template, values):
    """Show the same positions as ZPL without a third party preview service."""
    width, height = template["width"], template["height"]
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" role="img" aria-label="Label preview">',
             f'<rect width="{width}" height="{height}" fill="white"/>',
             f'<path d="M24 2 H{width-24}" stroke="#172620" stroke-width="4"/>']
    for field in template["fields"]:
        if field["checkbox"]:
            parts.append(f'<rect x="40" y="{field["y"]+4}" width="27" height="27" fill="none" stroke="#172620" stroke-width="3"/>')
        for index, line in enumerate(values[field["id"]]):
            y = field["y"] + field["font"] + index*field["font"]*1.15
            parts.append(f'<text x="{field["x"]}" y="{y}" font-family="Arial,sans-serif" font-weight="700" font-size="{field["font"]}" fill="#172620">{html.escape(line)}</text>')
    return "".join(parts) + "</svg>"


def send_to_printer(zpl):
    """Send a complete job to the configured raw TCP printer endpoint."""
    host = os.environ.get("PRINTER_HOST", "zd621.vanness.life")
    port = int(os.environ.get("PRINTER_PORT", "9100"))
    with socket.create_connection((host, port), timeout=5) as connection:
        connection.settimeout(5)
        connection.sendall(zpl.encode("ascii"))
