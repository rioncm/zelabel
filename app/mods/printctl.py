import yaml
import logging
import requests
import json
import socket
import copy
from mods.utility import ZplLabel
from mods.imgen import ZplImageGenerator as zig

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger(__name__)

# Load YAML config
with open("config.yaml", "r") as f:
    config = yaml.safe_load(f)["config"]
    logger.info("Loaded configuration from config.yaml")

printer = config["printer"]

class PrintCtl:
    """
    PrintCtl class handles the preparation and printing of labels.
    It fetches label data, prepares it according to templates, and sends it to the printer.
    """

    def __init__(self):
        self.printer = config["printer"]
        logger.info("PrintCtl initialized with printer config: %s", self.printer)

    def _prep_label(self, label_data: dict) -> dict:
        """
        Prepares a label based on the template and input data
        """
        logger.debug("Preparing label with data: %s", label_data)
        
        # Load templates configuration
        with open("config/templates.yaml") as f:
            templates = yaml.safe_load(f)["templates"]
        
        template_id = label_data.get("format", "default")
        if template_id not in templates:
            logger.warning(f"Template '{template_id}' not found, using default")
            template_id = "default"
            
        template = templates[template_id]
        
        # Create base document structure
        merged = {
            "properties": {
                "description": template.get("description", ""),
                "units": "mm",
                "width": 101.2,
                "height": 50.8,
                "margin-top": 3,
                "margin-bottom": 0,
                "margin-left": 5,
                "margin-right": 5,
                "copies": label_data.get("copies", 1)
            },
            "header": {},
            "body": {},
            "footer": {},
            "static": {}
        }
        
        # Process template fields
        for field in template["fields"]:
            field_id = field["id"]
            field_value = label_data["label"].get(field_id, "")
            field_style = field["style"]
            
            # Determine section based on field position
            section = "body"
            if field_style["start_y"] <= 8:
                section = "header"
            elif field_style["start_y"] >= 25:
                section = "footer"
                
            # Add field to appropriate section
            field_key = f"line{len(merged[section]) + 1}"
            merged[section][field_key] = {
                "text": field_value,
                "pre-text": "",
                "post-text": "",
                "add-var": "",
                "justify": field_style["justify"],
                "font_height": field_style["font_height"],
                "font_width": field_style["font_width"],
                "invert": False,
                "max_chars": field_style["max_chars"],
                "start-x": 0,
                "start-y": field_style["start_y"]
            }
            
            if "max_lines" in field_style:
                merged[section][field_key]["max_lines"] = field_style["max_lines"]

        # Add static date field
        merged["static"]["line1"] = {
            "text": "PRINTED: ",
            "add-var": "date",
            "justify": "L",
            "font_height": 2,
            "font_width": 2,
            "invert": False,
            "max_chars": 50,
            "start-x": 0,
            "start-y": 30
        }

        logger.debug("Merged label document: %s", merged)
        return merged

    def _print_label(self, zpl_data, copies=1, test=False):
        """
        Sends the ZPL data to the printer.
        """
        logger.info("Printing label. Copies: %d, Test mode: %s", copies, test)
        try:
            for i in range(copies):
                logger.debug("Printing copy %d/%d", i+1, copies)
                if test:
                    logger.info("Test mode enabled. Generating label image instead of printing.")
                    zig.generate_label(zpl_data)
                else:
                    logger.info("Sending ZPL data to printer at %s:%s", printer["ip"], printer["port"])
                    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                        sock.connect((printer["ip"], printer["port"]))
                        sock.sendall(zpl_data.encode('utf-8'))
                        logger.info("Label sent to printer successfully.")
                        sock.close()
        except Exception as e:
            logger.error("Error printing label: %s", e)
            return False
        
        return True

    def _render_label(self, label_data: dict) -> str:
        """
        Renders the label data into ZPL format.
        """
        logger.debug("Rendering label data to ZPL: %s", label_data)
        # Create a Utility instance
        label = ZplLabel(label_data["properties"], label_data)
        
        # Add text blocks to the label
        for section in ["header", "body", "footer", "static"]:
            if section in label_data:
                for line_key, line_data in label_data[section].items():
                    logger.debug("Adding text block from section '%s', line '%s': %s", 
                               section, line_key, line_data)
                    label.add_text_block(line_data)

        # Return the ZPL string
        zpl = label.get_label()
        logger.info("Label rendered to ZPL format.")
        return zpl
    
    def print_label(self, label_data: dict, test=False) -> bool:
        """
        Prepares and prints the label based on the provided label data.
        """
        logger.info("Starting label print process.")
        # Prepare the label data
        prepared_label = self._prep_label(label_data)
        
        # Render the label to ZPL format
        zpl_data = self._render_label(prepared_label)
        
        # Print the label
        result = self._print_label(zpl_data, copies=prepared_label["properties"]["copies"], 
                                 test=test)
        if result:
            logger.info("Label print process completed successfully.")
        else:
            logger.error("Label print process failed.")
        return result
