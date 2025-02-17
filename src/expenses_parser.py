from entry import Entries, Entry
from reference import References, Reference
from expense import Expenses


class Expenses_parser:
    def __init__(self):
        self.entries = None
        self.references = None
        self.sums = None

    def load(self, entries: Entries, references: References):
        self.entries = entries
        self.references = references
        self.sums = Expenses()

    def parse(self, update_references: bool = False):
        for entry in self.entries:
            matches = []
            for reference in self.references:
                for pattern in reference.patterns:
                    if pattern in entry.description:
                        matches.append(reference.classe_name)

            if len(matches) > 1:  # TODO Ne pas considéré si les matchs sont les mêmes
                print(
                    f"Plusieurs matchs rencontrés : {','.join(matches)} dans {entry.description}\nLe premier trouvé seulement sera considéré"
                )
            if len(matches) == 0:
                print(f"Aucune correspondance trouvée : {entry.description}")
                if update_references:
                    self.update_ref(entry)
                else:
                    self.sums.add_expense(entry)  # Ajout dans 'Autres'
            else:
                self.sums.add_expense(entry, category_name=matches[0])
        return self.sums

    def update_ref(self, entry):
        print(
            f"Quelle catégorie donner ?\n{'\n'.join([f"{ref.classe_index} -> {ref.classe_name}" for ref in self.references])}\n *class-name* -> custom reference)"
        )
        category = input()
        print(f"Quel mot clé associer ?")
        keyword = input()
        if category.isdigit():
            classname = self.references.get_classname_by_id(int(category))
            self.references.add_pattern(category, keyword)
            self.sums.add_expense(entry, category_name=classname)
        elif category:
            self.references.add_ref_fields(
                category, int(len(self.references)), [keyword]
            )
            self.sums.add_expense(entry, category_name=category)
        else:
            self.sums.add_expense(entry)  # Ajout dans 'Autres'
