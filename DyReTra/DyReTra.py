from DyReTra import config
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash

app = Flask(__name__)

app.config.update(
    DEBUG=config.DEBUG,
    SECRET_KEY=config.SECRET_KEY
)

@app.route('/')
def hello_world():
    return 'Hello, World!'