from zpl import Label
import requests
from datetime import datetime, timedelta, date
import logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger(__name__)

class ZplLabel:

    def __init__(self, props: dict, json_data):
        self.props = props
        self.json_data = json_data
        self.sections = ["header", "body", "footer", "static"]

        self.label = Label(self.props.get("label_width_mm", 100), self.props.get("label_height_mm", 50))
        self.margins = {
            "left": self.props.get("margin-left", 0),
            "right": self.props.get("margin-right", 0),
            "top": self.props.get("margin-top", 0),
            "bottom": self.props.get("margin-bottom", 0)
        }
        logger.info("Initialized ZplLabel with width=%s mm, height=%s mm, margins=%s", 
                    self.props.get("label_width_mm", 100), 
                    self.props.get("label_height_mm", 50), 
                    self.margins)

    def add_text_block(self, line_obj):
        """
        Add a text block to the label.
        """
        max_lines = line_obj.get("max_lines", 1)
        max_chars = line_obj.get("max_chars", 25)

        justify = line_obj.get("justify", "L")
        if justify not in ["L", "C", "R", "J"]:
            logger.warning("Unknown justification '%s', defaulting to 'L'", justify)
            justify = "L"
        text = str(line_obj.get("text", ""))
        pre_text = str(line_obj.get("pre-text", ""))
        post_text = str(line_obj.get("post-text", ""))
        text = f"{pre_text.ljust(1)} {text.ljust(1)} {post_text}"
        x = line_obj.get("start-x", 50)
        y = line_obj.get("start-y", 50) 

        h = int(line_obj.get("font_height", 5))
        w = int(line_obj.get("font_width", 5))
        invert = line_obj.get("invert", False)

        add_var = line_obj.get("add-var", "")
        if add_var == "date":
            text += date.today().strftime("%Y-%m-%d")
            logger.info("Added current date to text block.")

        logger.info("Adding text block at (%d, %d): '%s' (font: %dx%d, lines: %d, chars: %d, justify: %s, invert: %s)", 
                    x, y, text, h, w, max_lines, max_chars, justify, invert)

        self._add_line(text, h, w, x, y, invert, max_lines, max_chars, justify)

    def _add_line(self, text, h, w, x, y, invert, lines, max_chars, justify):
        logger.debug("Writing line to label at (%d, %d): '%s'", x, y, text)
        self.label.origin(x, y)
        # Invert functionality is not supported as field_reverse does not exist
        self.label.write_text(text, char_height=h, char_width=w, font='0', orientation='N',  line_width=100, max_line=lines, line_spaces=max_chars, justification="L", hanging_indent=0, qrcode=False)
        self.label.endorigin()
        logger.debug("Finished writing line to label.")

    def get_label(self):
        """
        Get the final label object in zpl.
        """
        logger.info("Dumping ZPL label output.")
        return self.label.dumpZPL()

class JSONBin:
    """
    A class to handle JSON data.
    """

    def __init__(self, bins: dict):
        self.bins = bins
        self.current_inbox = None

    
    # Extract headers correctly (YAML may interpret colons inside values as key-value)
    def extract_headers(self, bin):
        headers = {}
        for key, value in bin["headers"].items():
            if ":" in value:
                # If the value contains a colon, wrap it in quotes
                headers[key] = f'"{value}"'
            else:
                headers[key] = value
        return headers

    # Fetch JSON payload from jsonbin.io
   
    def fetch_labels(self):
        inbox = self.bins["inbox"]
        headers = self.extract_headers(self.bins["inbox"])
        try:
            url = f"{inbox['url']}/{inbox['version']}"
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            self.current_inbox = response.json()
            return response.json()["record"]["inbox"]
        except requests.RequestException as e:
            print(f"Error fetching label data: {e}")
            return None
    
        
    def clear_inbox(self):
        inbox = self.bins["inbox"]
        headers = self.extract_headers(self.bins["inbox"])
        base = {"inbox": {}}
        try:
            response = requests.put(inbox["url"], json=base, headers=headers)
            response.raise_for_status()
            return True
        except requests.RequestException as e:
            print(f"Error clearing label data: {e}")
            return False
  
    def mark_printed(self, label_id):
        inbox = self.current_inbox
        if not inbox:
            print("No inbox data available.")
            return False
        if label_id not in inbox:
            print(f"Label ID {label_id} not found in inbox.")
            return False
        inbox[label_id]["printed"] = True
        inbox[label_id]["print-date"] = date.today().strftime("%Y-%m-%d")
        return True
        



    # def archive(self):
    #     try:
    #         # 1. Get the latest inbox from JSONBin
    #         response = requests.get(self.bins["inbox"]["url"], headers=self.extract_headers(self.bins["inbox"]))
    #         response.raise_for_status()
    #         current_bin = response.json()["record"]
    #         inbox = current_bin.get("inbox", {})
    #     except requests.RequestException as e:
    #         print(f"Error fetching current inbox: {e}")
    #         return False

    #     # 2. Remove printed labels from the new inbox copy using self.current_inbox
    #     for label_id, label in self.current_inbox.get("inbox", {}).items():
    #         if label.get("printed"):
    #             inbox.pop(label_id, None)

    #     # 3. PUT the updated inbox back
    #     try:
    #         response = requests.put(self.bins["inbox"]["url"], headers=self.extract_headers(self.bins["inbox"]), json={"inbox": inbox})
    #         response.raise_for_status()
    #         print(f"Updated inbox with {len(inbox)} remaining unprinted labels.")
    #     except requests.RequestException as e:
    #         print(f"Error updating inbox: {e}")
    #         return False

    #     # 4. GET the printed bin
    #     try:
    #         response = requests.get(self.bins["printed"]["url"], headers=self.extract_headers(self.bins["printed"]))
    #         response.raise_for_status()
    #         printed_bin = response.json()["record"]
    #         printed = printed_bin.get("printed", {})
    #     except requests.RequestException as e:
    #         print(f"Error fetching printed bin: {e}")
    #         return False

    #     # 5. Remove printed entries older than 48 hours
    #     now = datetime.now()
    #     cutoff = now - timedelta(hours=48)
    #     filtered_printed = {}

    #     for label_id, label in printed.items():
    #         try:
    #             label_date = datetime.strptime(label.get("print-date", ""), "%Y-%m-%d")
    #             if label_date >= cutoff:
    #                 filtered_printed[label_id] = label
    #         except (ValueError, TypeError):
    #             # Skip label if date is invalid or missing
    #             continue

    #     # 6. Add printed labels from self.current_inbox
    #     for label_id, label in self.current_inbox.get("inbox", {}).items():
    #         if label.get("printed"):
    #             label["print-date"] = label.get("print-date", date.today().strftime("%Y-%m-%d"))
    #             filtered_printed[label_id] = label

    #     # 7. PUT the updated printed bin
    #     try:
    #         response = requests.put(
    #             self.bins["printed"]["url"],
    #             headers=self.extract_headers(self.bins["printed"]),
    #             json={"printed": filtered_printed}
    #         )
    #         response.raise_for_status()
    #         print(f"Archived {len(self.current_inbox.get('inbox', {}))} labels to printed bin.")
    #     except requests.RequestException as e:
    #         print(f"Error updating printed bin: {e}")
    #         return False

    #     # 8. Flush self.current_inbox
    #     self.current_inbox = {"inbox": {}}
    #     print("Flushed current inbox.")
    #     return True