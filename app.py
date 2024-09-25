import requests
from flask import Flask, render_template, url_for, request

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html")

@app.route("/Summarize", methods=["GET", "POST"])
def summarize():
    if request.method == "POST":
        try:
            data = request.form["data"]
            maxL = int(request.form["maxL"])
            minL = maxL // 4
        except KeyError:
            return "Error: Missing required form data", 400

        API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"
        headers = {"Authorization": f"Bearer {api_key}"}  # Use an environment variable or secure storage

        def query(payload):
            response = requests.post(API_URL, headers=headers, json=payload)
            response.raise_for_status()  # Raise an exception for 4xx or 5xx status codes
            return response.json()

        output = query({
            "inputs": data,
            "parameters": {"min_length": minL, "max_length": maxL},
        })[0]

        return render_template("index.html", result=output["summary_text"])
    else:
        return render_template("index.html")