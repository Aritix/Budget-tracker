## Rules classes and functions
import csv
import yaml


class Rule:
    def __init__(self, classe_name: str, classe_index: int, patterns: list):
        self.classe_name = classe_name
        self.classe_index = classe_index
        self.patterns = patterns
        self.goal = None

    def add_patterns(self, pattern: str):
        self.patterns.append(pattern)

    def save(self) -> str:
        return f"{self.classe_name}|{self.classe_index}|{','.join(self.patterns)}"

    def __str__(self):
        return (
            f"<Rule object {self.classe_name} ({self.classe_index}) : {self.patterns}>"
        )

    @classmethod
    def rule_from_list(cls, rule_list):
        class_name_index = 0
        classe_index = 1
        patterns_index = 2
        return Rule(
            classe_name=rule_list[class_name_index],
            classe_index=rule_list[classe_index],
            patterns=rule_list[patterns_index].split(","),
        )

    @classmethod
    def load(cls, name: str, rule_dict: dict):
        id = rule_dict["id"]
        kw = rule_dict["keywords"]
        return Rule(classe_name=name, classe_index=id, patterns=kw)


class Rules:
    def __init__(self):
        self.elements = []
        self.iteration = -1

    def add_rule_object(self, rule: Rule):
        self.elements.append(rule)

    def add_rule_fields(self, classe_name: str, classe_index: int, patterns: list):
        self.elements.append(
            Rule(classe_name=classe_name, classe_index=classe_index, patterns=patterns)
        )

    def add_pattern(self, class_index: str, pattern: str):
        found = False
        for ref in self.elements:
            if ref.classe_index == class_index:
                ref.add_patterns(pattern)
                found = True
        if not found:
            print("WARNING : No similar class index found !")

    def get_classname_by_id(self, class_index: int) -> str:
        for rule in self.elements:
            if rule.classe_index == class_index:
                return rule.classe_name

    def save(self, output_file: str = None) -> str:
        res = "\n".join([rule.save() for rule in self.elements])
        if output_file:
            with open(output_file, "w") as f:
                f.write(res)
        return res

    def __iter__(self):
        self.iteration = 0
        return self

    def __next__(self):
        if self.iteration >= len(self.elements):
            raise StopIteration
        iteration = self.elements[self.iteration]
        self.iteration += 1
        return iteration

    def __str__(self):
        return "Rules Object\n" + "\n".join(["|\t" + str(ref) for ref in self]) + "\n-"

    def __len__(self):
        return len(self.elements)

    @classmethod
    def load(cls, filename):
        with open(filename, "r") as file:
            dict_rules = yaml.safe_load(file)
        rules = Rules()
        for name, rule in dict_rules["categories"].items():
            rules.add_rule_object(Rule.load(name, rule))
        return rules
