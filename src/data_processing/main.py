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


# Parsing function

def main(input : list, rules_path : str, output_path, display: bool, update_refs: bool):
    """
    Begin the treatment of documents.

    -input : list of paths to the files or directories to parse
    -rules_path : path to the reference file
    -output_path : path to the output file to write in
    -display : boolean to display the graphs
    -update_refs : boolean to update the references
    """
    input_file_paths = []
    for path in input:
        if not os.path.exists(path):
            print("Error : one of the input paths does exists.")
            return 1
        if os.path.isdir(path):
            for entry in os.listdir(path):
                combined_path = os.path.join(path, entry)
                if os.path.splitext(entry)[1] == '.pdf' and os.path.isfile(combined_path):
                    input_file_paths.append(combined_path)
            print(f"Found {len(input_file_paths)} files.")
        elif os.path.isfile(path):
            input_file_paths.append(path)
        else:
            print("Error : Unexpected behaviour. The input is neither a file or a directory but does exist ?")
            return 1
    # Program launch
    entries = Entries()
    for file_path in input_file_paths:
        pdf_parser = parser_identifier(file_path)
        if pdf_parser:
            pdf_parser.load(file_path)
            entries.add_entries(pdf_parser.transform_to_entries())
    rules = Rules.load(rules_path)
    expense_parser = Expenses_parser()
    expense_parser.load(entries, rules)
    expenses = expense_parser.parse(update_rules=update_refs)
    expenses.all_graph(SavedFileName=output_path, show=display)
    return 1