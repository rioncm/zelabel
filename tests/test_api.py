import copy
from pathlib import Path
import tempfile

import yaml
import unittest
from unittest.mock import patch

from api.app import create_app
from api.config import ConfigError, load_config, validate_config
from api.labels import LabelError, prepare, render_svg, render_zpl
from api.templates import TEMPLATES


class LabelTests(unittest.TestCase):
    def setUp(self):
        self.config = yaml.safe_load(Path("config/zelabel.yaml").read_text())
        self.config["printers"]["zebra_small"].update(host="small.test", port=9200, dpi=300, top_offset_dots=0)
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.path = Path(self.temp.name) / "config.yaml"
        self.path.write_text(yaml.safe_dump(self.config))
        self.client = create_app(self.path).test_client()
        self.payload = {"template": "storage-box", "values": {"title": "Winter decor"}, "copies": 2}

    def test_all_templates_render_both_media_sizes(self):
        for template_id, template in TEMPLATES.items():
            required = {field["id"]: "Example" for field in template["fields"] if field["required"]}
            prepared, values, _ = prepare({"template": template_id, "values": required})
            for dpi in (203, 300):
                zpl = render_zpl(prepared, values, dpi=dpi)
                self.assertIn(f"^PW{round(template['width'] * dpi / 203)}", zpl)
                self.assertIn("^XZ", zpl)

    def test_validation_rejects_overflow_and_control_characters(self):
        for value in ("x" * 40, "Hello\n^XA", "Café"):
            with self.assertRaises(LabelError):
                prepare({"template": "storage-box", "values": {"title": value}})
        with self.assertRaises(LabelError):
            prepare({**self.payload, "copies": 11})

    def test_zpl_control_characters_are_escaped(self):
        template, values, _ = prepare({"template": "storage-box", "values": {"title": "A^B~C_D"}})
        zpl = render_zpl(template, values)
        self.assertIn("^FDA_5EB_7EC_5FD", zpl)
        self.assertNotIn("^FDA^B", zpl)

    def test_top_offset_moves_print_and_preview_within_label(self):
        template, values, _ = prepare({"template": "storage-box", "values": {"title": "Winter decor"}})
        for dpi in (203, 300):
            scaled = lambda value: round(value * dpi / 203)
            zpl = render_zpl(template, values, dpi=dpi, top_offset=24)
            self.assertIn(f"^FO{scaled(24)},{scaled(24)}^GB", zpl)
            self.assertIn(f"^FO{scaled(42)},{scaled(60)}^A0N", zpl)
            self.assertIn(f"^LL{scaled(template['height'])}", zpl)
        svg = render_svg(template, values, top_offset=24)
        self.assertIn('d="M24 26 H788"', svg)
        self.assertIn('x="42" y="118.0"', svg)

    def test_preview_escapes_html_and_never_prints(self):
        with patch("api.app.send_to_printer") as send:
            response = self.client.post("/api/preview", json={"template": "storage-box", "values": {"title": "A<B>"}})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"A&lt;B&gt;", response.data)
        send.assert_not_called()

    def test_print_requires_origin_and_reports_transport_failure(self):
        with patch("api.app.send_to_printer") as send:
            response = self.client.post("/api/print", json=self.payload)
            self.assertEqual(response.status_code, 403)
            send.assert_not_called()
        with patch("api.app.send_to_printer", side_effect=OSError("offline")):
            response = self.client.post("/api/print", json=self.payload, headers={"Origin": "https://labels.vanness.life"})
            self.assertEqual(response.status_code, 502)
        with patch("api.app.send_to_printer") as send:
            response = self.client.post("/api/print", json=self.payload, headers={"Origin": "https://labels.vanness.life"})
            self.assertEqual(response.status_code, 200)
            self.assertIn("^PQ2", send.call_args.args[0])

    def test_routes_every_template_and_applies_printer_calibration(self):
        for template_id, template in TEMPLATES.items():
            payload = {"template": template_id, "values": {
                field["id"]: "Example" for field in template["fields"] if field["required"]}}
            printer_id = "zebra_small" if template_id == "jar-can" else "zebra_large"
            printer = self.config["printers"][printer_id]
            with patch("api.app.send_to_printer") as send:
                response = self.client.post("/api/print", json=payload, headers={"Origin": "https://labels.vanness.life"})
                self.assertEqual(response.status_code, 200)
                self.assertEqual(response.json["printer"]["id"], printer_id)
                self.assertEqual(send.call_args.args[1], printer)
                prepared, values, copies = prepare(payload)
                self.assertEqual(send.call_args.args[0], render_zpl(prepared, values, copies, printer["dpi"], printer["top_offset_dots"]))
            preview = self.client.post("/api/preview", json=payload)
            self.assertEqual(preview.data.decode(), render_svg(prepared, values, printer["top_offset_dots"]))

    def test_public_destinations_omit_network_settings(self):
        response = self.client.get("/api/templates")
        for template in response.json["templates"]:
            self.assertEqual(set(template["printer"]), {"id", "name"})
        self.assertNotIn("small.test", response.data.decode())

    def test_invalid_configuration_fails_at_startup(self):
        invalid = [None, {}, {**self.config, "version": True}]
        for key, value in (("host", "REPLACE_WITH_HOST"), ("host", ""), ("port", True),
                           ("port", 65536), ("dpi", 600), ("top_offset_dots", 25),
                           ("top_offset_dots", -1), ("media", "3x2")):
            config = copy.deepcopy(self.config)
            config["printers"]["zebra_small"][key] = value
            invalid.append(config)
        for routes in ({"4x2": "zebra_large"}, {"4x2": "zebra_large", "2x2": "missing"},
                       {"4x2": "zebra_large", "2x2": "zebra_large"}):
            invalid.append({**self.config, "routing": routes})
        for config in invalid:
            with self.subTest(config=config), self.assertRaises(ConfigError):
                validate_config(config)
        with self.assertRaises(ConfigError):
            create_app("/nonexistent/zelabel.yaml")
        self.path.write_text("printers: [invalid")
        with self.assertRaises(ConfigError):
            create_app(self.path)

    def test_config_is_read_once_and_environment_selects_file(self):
        with patch.dict("os.environ", {"ZELABEL_CONFIG": str(self.path)}):
            self.assertEqual(load_config(), self.config)
        self.path.write_text("invalid")
        self.assertEqual(self.client.get("/api/templates").status_code, 200)

    def test_request_cannot_override_configured_destination(self):
        payload = {**self.payload, "printer": "zebra_small", "host": "untrusted.test"}
        with patch("api.app.send_to_printer") as send:
            response = self.client.post("/api/print", json=payload, headers={"Origin": "https://labels.vanness.life"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(send.call_args.args[1], self.config["printers"]["zebra_large"])

    def test_configmap_matches_example_and_is_mounted(self):
        resources = list(yaml.safe_load_all(Path("k8s/zelabel.yaml").read_text()))
        configmap = next(item for item in resources if item["kind"] == "ConfigMap")
        self.assertEqual(yaml.safe_load(configmap["data"]["config.yaml"]),
                         yaml.safe_load(Path("config/zelabel.yaml").read_text()))
        deployment = next(item for item in resources if item["kind"] == "Deployment")
        pod = deployment["spec"]["template"]["spec"]
        api = next(item for item in pod["containers"] if item["name"] == "api")
        mount = api["volumeMounts"][0]
        volume = next(item for item in pod["volumes"] if item["name"] == mount["name"])
        self.assertEqual(volume["configMap"]["name"], configmap["metadata"]["name"])
        self.assertTrue(mount["readOnly"])
        self.assertEqual(next(item["value"] for item in api["env"] if item["name"] == "ZELABEL_CONFIG"),
                         mount["mountPath"] + "/config.yaml")

    def test_transport_uses_selected_endpoint(self):
        from api.labels import send_to_printer
        printer = self.config["printers"]["zebra_small"]
        with patch("api.labels.socket.create_connection") as connect:
            send_to_printer("^XA^XZ", printer)
            connect.assert_called_once_with(("small.test", 9200), timeout=5)
            connect.return_value.__enter__.return_value.sendall.assert_called_once_with(b"^XA^XZ")


if __name__ == "__main__":
    unittest.main()
