import os
from flask import Flask, render_template, flash, request, redirect, url_for, send_file
from src.data_processing.main import main
from werkzeug.utils import secure_filename
import random
import time

UPLOAD_FOLDER = "/tmp/BudViz/uploads"
ALLOWED_EXTENSIONS = {"pdf", ".txt"}

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


@app.route("/")
def hello_world():
    return render_template("index.html")


@app.route("/upload", methods=["GET", "POST"])
def upload():
    token = time.strftime("%Y_%m_%d_%H_%M_%S_") + str(random.randint(0, 1000))
    temp_path = os.path.join(app.config["UPLOAD_FOLDER"], token)
    file_paths = []
    if not os.path.exists(temp_path):
        os.makedirs(temp_path)
    if request.method == "POST":
        files = request.files.getlist("inputs")
        reference = request.files.get("reference")
        if reference:
            reference.save(os.path.join(temp_path, reference.filename))
        reference_path = os.path.join(temp_path, reference.filename)
        for file in files:
            filename = secure_filename(file.filename)
            file.save(os.path.join(temp_path, filename))
            file_paths.append(os.path.join(temp_path, filename))
    output_path = os.path.join(app.config["UPLOAD_FOLDER"], token, "output.png")
    main(file_paths, reference_path, output_path, False, False)

    return send_file(output_path)
