# copie colle un format csv, indique les colonnes de prix, description, date
# Fournit une liste de mot-clé d'attribution d'entrées dans des catégories
# Parse les entrées, donne les sommes et possibilités de construire les grqphiques temporels
from entry import Entries, Entry
from reference import References, Reference
from expense import Expenses
from BNC_MasterCard_parser import BNC_MasterCard_parser
from expenses_parser import Expenses_parser
import argparse


# Parsing function

def main():
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
    input_arg = args.input
    display_arg = args.display
    output_arg = args.output
    references_arg = args.references
    update_refs_arg = args.update_refs

    # Argument verification

    # Program launch
    pdf_parser = BNC_MasterCard_parser()
    pdf_parser.load(input_arg)
    entries = pdf_parser.transform_to_entries()
    references = References.import_from_file(references_arg)
    expense_parser = Expenses_parser()
    expense_parser.load(entries, references)
    expenses = expense_parser.parse(update_references=update_refs_arg)

    SavedFileName = output_arg

    expenses.all_graph(SavedFileName=output_arg, show=display_arg)



if __name__ == "__main__":
    # entries_file_name = "data/2025-02.txt"
    # references_file_name = "data/references.txt"

    # refs = References.import_from_file(references_file_name)
    # entries = Entries.import_from_file(entries_file_name)

    # expenses = parse(entries, refs)
    # # expenses.time_graph(SavedFileName="fevrier.svg")
    # # expenses.pie_graph()
    # expenses.all_graph()

    main()
