# copie colle un format csv, indique les colonnes de prix, description, date
# Fournit une liste de mot-clé d'attribution d'entrées dans des catégories
# Parse les entrées, donne les sommes et possibilités de construire les grqphiques temporels
from entry import Entries, Entry
from reference import References, Reference
from expense import Expenses
from BNC_MasterCard_parser import BNC_MasterCard_parser
import argparse


# Parsing function


def parse(
    entries: Entries,
    references: References,
):
    sums = Expenses()
    for entry in entries:
        matches = []
        for reference in references:
            for pattern in reference.patterns:
                if pattern in entry.description:
                    matches.append(reference.classe_name)

        if len(matches) > 1:  # TODO Ne pas considéré si les matchs sont les mêmes
            print(
                f"Plusieurs matchs rencontrés : {','.join(matches)} dans {entry.description}\nLe premier trouvé seulement sera considéré"
            )
        if len(matches) == 0:
            print(f"Aucune correspondance trouvée : {entry.description}")
            sums.add_expense(entry)
        else:
            sums.add_expense(entry, category_name=matches[0])
    return sums


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

    # Argument parsing
    args = parser.parse_args()
    input_arg = args.input
    display_arg = args.display
    output_arg = args.output
    references_arg = args.references

    # Argument verification

    # Program launch
    parser = BNC_MasterCard_parser()
    parser.load(input_arg)
    entries = parser.transform_to_entries()
    references = References.import_from_file(references_arg)
    expenses = parse(entries, references)


    SavedFileName = output_arg

    expenses.all_graph(SavedFileName=output_arg, show=display_arg)

    print(input_arg, display_arg, output_arg)


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
