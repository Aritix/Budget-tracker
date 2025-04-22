from flask import Blueprint, render_template, abort, request, current_app, Response
from src.data_processing.main import *
import json
import os

api = Blueprint('api', __name__, url_prefix='/api')

@api.route('/upload', methods=['POST'])
def upload():
    """
    API route for uploading new files
    """
    ...

@api.route('/category', methods=['GET', 'POST'])
@api.route('/category/', methods=['GET', 'POST'])
@api.route('/category/<category_name>', methods=['GET', 'POST', 'DELETE', 'PUT'])
def category(category_name: str =None):
    """
    API route for viewing and editing categories.
    """
    if current_app.config["environment"] == "TEST":
        expenses_filename = "data/test/expenses_test.yaml"
    elif current_app.config["environment"] == "PROD":
        expenses_filename = "expenses.yml"
    else:
        expenses_filename = "expenses.yml"
        raise 'No environment detected'
    print(f"/category : {category_name}")
    if request.method == "GET":
        # List the categories
        expenses = load_objects(filename = expenses_filename)
        return json.dumps(expenses.categories)
    elif request.method == "POST":
        # Add a new category
        # TODO manage better default values
        data: dict = json.loads(request.data)
        new_category_name = data['name']
        new_category_goal = data['goal'] if 'goal' in data.keys() else 0
        expenses = load_objects(filename = expenses_filename)
        expenses.add_rule_fields(new_category_name, 1, [])
        expenses.save(filename = expenses_filename)
        return Response(status=204)
    elif request.method == "PUT":
        # Edit a category characteristics
        data: dict = json.loads(request.data)
        changes = data
        expenses = load_objects(filename = expenses_filename)
        expenses.edit_rule(category_name, changes)
        expenses.save(filename = expenses_filename)
        return Response(status=204)
    elif request.method == "DELETE":
        # Delete the category
        # category_name = request.data['name']
        expenses = load_objects(filename = expenses_filename)
        print(len(expenses.rules))
        expenses.delete_rule(category_name)
        expenses.save(filename = expenses_filename)
        return Response(status=204)
    return Response(status=418)

@api.route('/category/<category_name>/keywords/', methods=['GET', 'POST', 'PUT', 'DELETE'])
def keyword(category_name):
    """
    API route for viewing, editing, adding and deleting keywords.
    """
    if request.method == "GET":
        "List the keywords for this category"
    elif request.method == "POST":
        "Add the keyword to the category"
        "List the keywords for this category"
    elif request.method == "PUT":
        "Edit the keyword to the category" #?
    elif request.method == "DELETE":
        "Delete the keyword"