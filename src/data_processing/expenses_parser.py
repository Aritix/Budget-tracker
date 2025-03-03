from src.data_processing.entry import Entries, Entry
from src.data_processing.rule import Rules, Rule
from src.data_processing.expense import Expenses


class Expenses_parser:
    def __init__(self):
        self.entries = None
        self.rules = None
        self.sums = None

    def load(self, entries: Entries, rules: Rules):
        self.entries = entries
        self.rules = rules
        self.sums = Expenses()

    def parse(self, update_rules: bool = False):
        for entry in self.entries:
            matches = []
            for rule in self.rules:
                for pattern in rule.patterns:
                    if pattern.upper() in entry.description.upper():
                        matches.append(rule.classe_name)

            if len(matches) > 1:  # TODO Ne pas considéré si les matchs sont les mêmes
                print(
                    f"Plusieurs matchs rencontrés : {','.join(matches)} dans {entry.description}\nLe premier trouvé seulement sera considéré"
                )
            if len(matches) == 0:
                print(f"Aucune correspondance trouvée : {entry.description}")
                if update_rules:
                    self.update_ref(entry)
                else:
                    self.sums.add_expense(entry)  # Ajout dans 'Autres'
            else:
                self.sums.add_expense(entry, category_name=matches[0])
        return self.sums

    def update_ref(self, entry):
        print(
            f"Quelle catégorie donner ?\n{'\n'.join([f"{ref.classe_index} -> {ref.classe_name}" for ref in self.rules])}\n *class-name* -> custom rule)"
        )
        category = input()
        print(f"Quel mot clé associer ?")
        keyword = input()
        if category.isdigit():
            classname = self.rules.get_classname_by_id(int(category))
            self.rules.add_pattern(category, keyword)
            self.sums.add_expense(entry, category_name=classname)
        elif category:
            self.rules.add_ref_fields(
                category, int(len(self.rules)), [keyword]
            )
            self.sums.add_expense(entry, category_name=category)
        else:
            self.sums.add_expense(entry)  # Ajout dans 'Autres'
