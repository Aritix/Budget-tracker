import os
from flask import Flask, render_template, flash, request, redirect, url_for, send_file
from src.data_processing.main import main, filter, getMetaData
from werkzeug.utils import secure_filename
import random
import time
import json

UPLOAD_FOLDER = "/tmp/BudViz/uploads"
ALLOWED_EXTENSIONS = {"pdf", ".txt"}

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


@app.route("/")
def hello_world():
    return render_template("inputs.html")


@app.route("/upload", methods=["GET", "POST"])
def upload():
    # token = time.strftime("%Y_%m_%d_%H_%M_%S_") + str(random.randint(0, 1000))
    # temp_path = os.path.join(app.config["UPLOAD_FOLDER"], token)
    if request.method == "POST":
        files = request.files.getlist("inputs")
        rules = request.files.get("reference")
    output_path = "outputs.csv"
    main(files, rules, output_path, False, False)

    return render_template("data.html")

@app.route("/getFilteredData", methods=["POST"])
def getFilteredDataRoute():
    """
    Route handler for sending the filtered data to the frontend.
    """
    time_filter = request.get_json()['time_filter']
    category_filter = request.get_json()['category_filter']
    new_expense = filter(time_filter, category_filter)

    return {
        'categories' : json.dumps(new_expense.get_category_json()),
        'months' : json.dumps(new_expense.get_months_json())
    }

@app.route("/getMetaData", methods=["GET"])
def getMetaDataRoute():
    """
    Route handler for sending the metadata to the frontend.
    *Should not be used for now*
    """
    metada = getMetaData()
    CategoriesNames = metada['categories']
    months = metada['months']
    return {
        'categories' : json.dumps(CategoriesNames),
        'months' : json.dumps(months)}