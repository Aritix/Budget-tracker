import os
from flask import Flask, render_template, flash, request, redirect, url_for, send_file
from src.data_processing.main import main, filter, getMetaData, getUncategorizedEntries, load, updateRules
from src.backend.api import api
from src.data_processing.expense import Expenses#, expenses_representer, expenses_constructor
from werkzeug.utils import secure_filename
import json
import yaml

UPLOAD_FOLDER = "/tmp/BudViz/uploads"
ALLOWED_EXTENSIONS = {"pdf", ".txt"}

app = Flask(__name__)
app.register_blueprint(api)
app.config["environment"] = "PROD"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
# Configuration


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

    cat_pos, cat_neg = new_expense.get_category_json()
    mon_pos, mon_neg = new_expense.get_months_json()
    return {
        'incomes' : {
            'categories' : list(cat_neg.keys()),
            'categorie_sums' : list(map(lambda x : -x, list(cat_neg.values()))),
            'months' : list(mon_neg.keys()),
            'month_sums' : list(map(lambda x : -x, list(mon_neg.values())))
        },
        'outcomes' : {
            'categories' : list(cat_pos.keys()),
            'categorie_sums' : list(cat_pos.values()),
            'months' : list(mon_pos.keys()),
            'month_sums' : list(mon_pos.values())
        }
    }

@app.route("/getMetaData", methods=["GET"])
def getMetaDataRoute():
    """
    Route handler for sending the metadata to the frontend.
    *Should not be used for now*
    """
    CategoriesNames = metada['categories']
    months = metada['months']
    return {
        'incomes' : {
            'categories' : json.dumps(CategoriesNames),
            'months' : json.dumps(months)},
        'outcomes' : {
            'categories' : json.dumps(CategoriesNames),
            'months' : json.dumps(months)}
    }
        
@app.route("/rules", methods=["GET", "POST"])
def getRules():
    """
    Route handler for the *rules* page.
    """
    return render_template("rules.html")


@app.route("/addKeywords", methods=["POST"])
def addKeywords():
    # print(type(request.data), json.loads(request.data))
    # print(updateRules(json.loads(request.data)))
    updateRules(json.loads(request.data))
    return 'yes'

@app.route("/UncategorizedEntries", methods=["GET"])
def uncategorizedEntries():
    return getUncategorizedEntries()

@app.route("/categories", methods=["GET"])
def getCategories():
    expenses = Expenses.load()
    categories = expenses.categories
    return json.dumps(categories)
    