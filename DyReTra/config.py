from flask import Flask
from config_values import *

app = Flask(__name__, static_url_path='/static')
app.config.from_object(__name__)
app.config.update(
    DEBUG=DEBUG,
    SECRET_KEY=SECRET_KEY
)
