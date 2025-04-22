# copie colle un format csv, indique les colonnes de prix, description, date
# Fournit une liste de mot-clé d'attribution d'entrées dans des catégories
# Parse les entrées, donne les sommes et possibilités de construire les grqphiques temporels
from src.data_processing.entry import Entries, Entry
from src.data_processing.rule import Rules, Rule
from src.data_processing.expense import Expenses
from src.data_processing.BNC_MasterCard_parser import BNC_MasterCard_parser
from src.data_processing.expenses_parser import Expenses_parser
from src.data_processing.parser_identifier import parser_identifier
from src.data_processing.main import main, test
import os
import argparse


# Parsing function

def cli_entrypoint():
    parser = argparse.ArgumentParser(
        prog="Budget Parser",
        description="A program to parse bank statements and track your expenses.",
    )

    # Add arguments
    parser.add_argument(
        "input",
        help="Path to the file to parse or directory containing the files to parse",
    )
    parser.add_argument(
        "-r",
        "--references",
        help="Path to the reference file.",
        default="references.txt",
    )
    parser.add_argument("-o", "--output", help="")
    parser.add_argument("-d", "--display", help="", action="store_true")
    parser.add_argument("--update-refs", help="", action="store_true")

    # Argument parsing
    args = parser.parse_args()
    display_arg = args.display
    output_arg = args.output
    references_arg = args.references
    update_refs_arg = args.update_refs
    input_arg = args.input
    input_file = []
    rule_file = open(references_arg, 'r')

    if os.path.isdir(input_arg):
        pass
    else:
        input_file.append(open(input_arg, "r"))

    # Argument verification

    main(input_file, rule_file, output_arg, display_arg, update_refs_arg)



if __name__ == "__main__":
    test()
    # cli_entrypoint()
