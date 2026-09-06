from flask import Flask

app = Flask(__name__)

@app.route("/")
def index():
    return "Placeholder for Recepio a food recipe app for the course TiKaWe."