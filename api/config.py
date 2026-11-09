"""Load and validate printer routing once when the API starts."""

import os
from pathlib import Path

import yaml

from .templates import TEMPLATES


class ConfigError(ValueError):
    """The runtime configuration cannot safely route label jobs."""


def load_config(path=None):
    path = path or os.environ.get("ZELABEL_CONFIG", "config/zelabel.yaml")
    try:
        with Path(path).open() as source:
            config = yaml.safe_load(source)
    except (OSError, yaml.YAMLError) as error:
        raise ConfigError(f"Cannot load ZeLabel configuration at {path}: {error}") from error
    return validate_config(config)


def validate_config(config):
    if not isinstance(config, dict) or set(config) != {"version", "printers", "routing"}:
        raise ConfigError("Configuration must contain version, printers, and routing only.")
    if type(config["version"]) is not int or config["version"] != 1:
        raise ConfigError("Configuration version must be 1.")
    printers, routing = config["printers"], config["routing"]
    if not isinstance(printers, dict) or not printers:
        raise ConfigError("Configure at least one printer.")
    media = {template["size"].replace("×", "x") for template in TEMPLATES.values()}
    for printer_id, printer in printers.items():
        if not isinstance(printer_id, str) or not printer_id.strip():
            raise ConfigError("Printer IDs must be nonempty strings.")
        if not isinstance(printer, dict) or set(printer) != {"name", "host", "port", "dpi", "media", "top_offset_dots"}:
            raise ConfigError(f"Printer {printer_id}: expected name, host, port, dpi, media, top_offset_dots.")
        for key in ("name", "host"):
            value = printer[key]
            if not isinstance(value, str) or not value.strip() or value != value.strip():
                raise ConfigError(f"Printer {printer_id}: {key} must be nonempty text without surrounding whitespace.")
        if "REPLACE_WITH_" in printer["host"] or any(c.isspace() for c in printer["host"]) or "/" in printer["host"]:
            raise ConfigError(f"Printer {printer_id}: supply a real hostname or IP address.")
        for key, low, high in (("port", 1, 65535), ("top_offset_dots", 0, 24)):
            if type(printer[key]) is not int or not low <= printer[key] <= high:
                raise ConfigError(f"Printer {printer_id}: {key} must be an integer from {low} to {high}.")
        if type(printer["dpi"]) is not int or printer["dpi"] not in (203, 300):
            raise ConfigError(f"Printer {printer_id}: dpi must be 203 or 300.")
        if not isinstance(printer["media"], str) or printer["media"] not in media:
            raise ConfigError(f"Printer {printer_id}: unsupported media size.")
    if not isinstance(routing, dict) or set(routing) != media:
        raise ConfigError("Routing must define every supported media size: " + ", ".join(sorted(media)))
    for size, printer_id in routing.items():
        if not isinstance(printer_id, str) or printer_id not in printers:
            raise ConfigError(f"Route {size}: unknown printer.")
        if printers[printer_id]["media"] != size:
            raise ConfigError(f"Route {size}: printer media does not match.")
    return config


def printer_for(config, template):
    printer_id = config["routing"][template["size"].replace("×", "x")]
    return printer_id, config["printers"][printer_id]
