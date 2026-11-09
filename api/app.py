"""Same-origin API, reachable externally only through the OIDC proxy."""

import logging
import os

from flask import Flask, Response, jsonify, request

from .config import load_config, printer_for
from .labels import LabelError, prepare, render_svg, render_zpl, send_to_printer
from .templates import TEMPLATES, public_templates

log = logging.getLogger(__name__)


def create_app(config_path=None):
    """Validate configuration before serving any requests."""
    config = load_config(config_path)
    app = Flask(__name__)
    app.config["MAX_CONTENT_LENGTH"] = 8192

    def destination(template):
        printer_id, printer = printer_for(config, template)
        return {"id": printer_id, "name": printer["name"]}

    @app.get("/api/healthz")
    def healthz():
        return jsonify(status="ok")

    @app.get("/api/templates")
    def templates():
        items = public_templates()
        for item in items:
            item["printer"] = destination(TEMPLATES[item["id"]])
        return jsonify(templates=items)

    @app.post("/api/preview")
    def preview():
        try:
            template, values, _ = prepare(request.get_json(silent=True))
            _, printer = printer_for(config, template)
            return Response(render_svg(template, values, printer["top_offset_dots"]), mimetype="image/svg+xml", headers={"Cache-Control": "no-store"})
        except (LabelError, ValueError) as error:
            return jsonify(error=str(error)), 400

    @app.post("/api/print")
    def print_label():
        if request.headers.get("Origin") != os.environ.get("APP_ORIGIN", "https://labels.vanness.life"):
            return jsonify(error="Invalid request origin."), 403
        try:
            template, values, copies = prepare(request.get_json(silent=True))
            printer_id, printer = printer_for(config, template)
            zpl = render_zpl(template, values, copies, printer["dpi"], printer["top_offset_dots"])
        except (LabelError, ValueError) as error:
            return jsonify(error=str(error)), 400
        try:
            send_to_printer(zpl, printer)
        except OSError:
            log.exception("Printer connection failed: %s", printer_id)
            return jsonify(error=f"{printer['name']} unavailable. Check that it is online, then retry."), 502
        log.info("Sent template=%s copies=%s printer=%s", request.json["template"], copies, printer_id)
        return jsonify(status="sent", copies=copies, printer=destination(template))

    return app
