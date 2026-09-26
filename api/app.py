"""Same-origin API, reachable externally only through the OIDC proxy."""

import logging
import os

from flask import Flask, Response, jsonify, request

from .labels import LabelError, prepare, render_svg, render_zpl, send_to_printer
from .templates import public_templates

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 8192
log = logging.getLogger(__name__)


@app.get("/api/healthz")
def healthz():
    return jsonify(status="ok")


@app.get("/api/templates")
def templates():
    return jsonify(templates=public_templates())


@app.post("/api/preview")
def preview():
    try:
        template, values, _ = prepare(request.get_json(silent=True))
        return Response(render_svg(template, values), mimetype="image/svg+xml", headers={"Cache-Control": "no-store"})
    except LabelError as error:
        return jsonify(error=str(error)), 400


@app.post("/api/print")
def print_label():
    if request.headers.get("Origin") != os.environ.get("APP_ORIGIN", "https://labels.vanness.life"):
        return jsonify(error="Invalid request origin."), 403
    try:
        template, values, copies = prepare(request.get_json(silent=True))
        zpl = render_zpl(template, values, copies, int(os.environ.get("PRINTER_DPI", "203")))
    except (LabelError, ValueError) as error:
        return jsonify(error=str(error)), 400
    try:
        send_to_printer(zpl)
    except OSError:
        log.exception("Printer connection failed")
        return jsonify(error="Printer unavailable. Check that it is online, then retry."), 502
    log.info("Sent template=%s copies=%s", request.json["template"], copies)
    return jsonify(status="sent", copies=copies)
