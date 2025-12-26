import requests
import shutil
from datetime import datetime
import pathlib
alphabet = ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z",]

class ZplImageGenerator:

    @staticmethod
    def generate_label(zpl_data: str) -> str:
        """
        Converts ZPL data to a PNG image using the Labelary API.
        """

        # Define the Labelary API URL with parameters for print density, label size, and index
        url = 'http://api.labelary.com/v1/printers/8dpmm/labels/4x2/0/'
        files = {'file': zpl_data}  # Expects string data

        # Send the ZPL data to the Labelary API
        response = requests.post(url, files=files, stream=True)

        # Generate a timestamped file name for the output image
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        file_name = f'label_{timestamp}.png'

        # Define the directory to save the label image
        labels_dir = pathlib.Path(__file__).parent.parent / 'labels'
        labels_dir.mkdir(parents=True, exist_ok=True)
        file_path = labels_dir / file_name
        # Ensure the file path is unique
        alphachar = 0
        while file_path.exists():
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            file_name = f'label_{timestamp}_{alphabet[alphachar]}.png'
            file_path = labels_dir / file_name
            alphachar += 1
            if alphachar > 25:
                break

        # Handle the API response
        if response.status_code == 200:
            response.raw.decode_content = True
            with open(file_path, 'wb') as out_file:
                shutil.copyfileobj(response.raw, out_file)
            return str(file_path)  # Return the file path as a string
        else:
            raise Exception(f"Error: {response.status_code} - {response.text}")
