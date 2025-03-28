from src.data_processing.entry import Entries, Entry
from src.data_processing.rule import Rules, Rule
from src.data_processing.expense import Expenses


class Expenses_parser:
    def __init__(self):
        self.entries: Entries = Entries()
        self.rules: Rules = Rules()
        self.expenses: Expenses = Expenses()

    def load(self, entries: Entries, rules: Rules, expenses: Expenses):
        self.entries = entries
        self.rules = rules
        self.expenses = expenses

    def parse(self, update_rules: bool = False, update_categorized: bool = True) -> Expenses:
        for entry in self.expenses.entries:
            if (entry.category == self.expenses.rules.default) or update_categorized:
                matches = []
                for rule in self.expenses.rules:
                    for pattern in rule.patterns:
                        if pattern.upper() in entry.description.upper():
                            matches.append(rule.classe_name)
                if len(matches) > 1 and not matches.count(matches[0]) == len(matches):
                    print(
                        f"Plusieurs matchs rencontrés : {','.join(matches)} dans {entry.description}.Le premier trouvé seulement sera considéré"
                    )
                elif len(matches) == 0:
                    if update_rules:
                        self.update_ref(entry)
                    else:
                        self.expenses.add_expense(entry, category_name=self.expenses.rules.default)  # Ajout dans la catégorie par défaut
                else:
                    self.expenses.add_expense(entry, category_name=matches[0])
        return self.expenses

    def parse_uncategorized(self):
        self.parse(update_categorized=False)

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
            self.expenses.add_expense(entry, category_name=classname)
        elif category:
            self.rules.add_ref_fields(
                category, int(len(self.rules)), [keyword]
            )
            self.expenses.add_expense(entry, category_name=category)
        else:
            self.expenses.add_expense(entry)  # Ajout dans 'Autres'
