import logging
from flask import Flask, request, jsonify, render_template
import yaml
from mods.printctl import PrintCtl

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = Flask(__name__)
print_ctl = PrintCtl()
# Initialize the print controller
logger.info("PrintCtl initialized for Flask app.")

@app.route('/')
@app.route('/create.html')
def create():
    logger.info("Rendering create label page.")
    return render_template('html/create.html')

@app.route('/api/v1/templates')
def get_templates():
    try:
        with open('config/templates.yaml', 'r') as f:
            templates = yaml.safe_load(f)
        return jsonify(templates)
    except Exception as e:
        logger.error(f"Error loading templates: {e}")
        return jsonify({"error": "Failed to load templates"}), 500

@app.route('/api/v1/print', methods=['POST'])
def print_label():
    data = request.get_json()
    print(data)
    if not data:
        logger.warning("No data provided in print API request.")
        return jsonify({'error': 'No data provided'}), 400
    else:
        logger.info(f"Received data for printing: {data}")
        try:
            result = print_ctl.print_label(data)
            if result:
                logger.info("Label printed successfully.")
                return jsonify({'status': 'success', 'message': 'Label printed successfully'}), 200
            else:
                logger.error("Failed to print label.")
                return jsonify({'status': 'error', 'message': 'Failed to print label'}), 500
        except Exception as e:
            logger.exception(f"Exception occurred while printing label: {e}")
            return jsonify({'status': 'error', 'message': 'Internal server error'}), 500

if __name__ == '__main__':
    logger.info("Starting Flask app on 0.0.0.0:5000")
    app.run(debug=True, host='0.0.0.0', port=8001)  # Adjust the port as needed
