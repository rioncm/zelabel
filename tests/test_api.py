import os
import unittest
from unittest.mock import patch

from api.app import app
from api.labels import LabelError, prepare, render_zpl
from api.templates import TEMPLATES


class LabelTests(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
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


if __name__ == "__main__":
    unittest.main()
