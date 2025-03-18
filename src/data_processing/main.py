# copie colle un format csv, indique les colonnes de prix, description, date
# Fournit une liste de mot-clé d'attribution d'entrées dans des catégories
# Parse les entrées, donne les sommes et possibilités de construire les grqphiques temporels
from src.data_processing.entry import Entries, Entry
from src.data_processing.rule import Rules, Rule
from src.data_processing.expense import Expenses
from src.data_processing.BNC_MasterCard_parser import BNC_MasterCard_parser
from src.data_processing.expenses_parser import Expenses_parser
from src.data_processing.parser_identifier import parser_identifier
import os
import argparse


def main(files : list, rules : str, output_path, display: bool, update_refs: bool):
    """
    Begin the treatment of documents.

    -input : list of paths to the files or directories to parse
    -rules_path : path to the reference file
    -output_path : path to the output file to write in
    -display : boolean to display the graphs
    -update_refs : boolean to update the references
    """
    # Program launch
    entries = Entries()
    for file in files:
        pdf_parser = parser_identifier(file)
        if pdf_parser:
            pdf_parser.load(file)
            entries.add_entries(pdf_parser.transform_to_entries())
    rules = Rules.load(rules)
    expense_parser = Expenses_parser()
    expense_parser.load(entries, rules)
    expenses = expense_parser.parse(update_rules=update_refs)
    expenses.all_graph(show=display)
    expenses.save()
    expenses.export_to_spreadsheet()
    return 1


def filter(time_filter: list, category_filter: list) -> Expenses:
    """
    Filter the data according to the filters.

    -time_filter : string of the time filter
    -category_filter : string of the category filter
    """
    expenses = Expenses.load("outputs.json")
    filtered_expenses = expenses.filter(time_filter, category_filter)
    return filtered_expenses

def getMetaData() -> dict:
    """
    Get the categories and months of the expenses.
    """
    expenses = Expenses.load("outputs.json")
    categories = expenses.get_category_json()
    categories = [k for k in categories.keys() if categories[k] > 0]
    months = expenses.get_months_json()
    months = [k for k in months.keys() if months[k] > 0]
    return {"categories": categories, "months": months}
