from waitress import serve
from .app import create_app

serve(create_app(), host="127.0.0.1", port=8001, threads=4)
