## Rules classes and functions
import csv
import yaml
from typing import Self
from yaml import CLoader as Loader, CDumper as Dumper


# Custom Representer
def my_class_representer(dumper, data):
    return dumper.represent_mapping("!MyClass", data.__getstate__())


# Custom Constructor
def my_class_constructor(loader, node):
    state = loader.construct_mapping(node)
    obj = MyClass(None, None)  # Create an instance with dummy values
    obj.__setstate__(state)
    return obj


class Rule:
    def __init__(self, classe_name: str, classe_index: int, patterns: list):
        self.classe_name = classe_name
        self.classe_index = classe_index
        self.patterns = patterns
        self.goal = 0

    def add_patterns(self, pattern: str):
        self.patterns.append(pattern)

    def save(self) -> str:
        return f"{self.classe_name}|{self.classe_index}|{','.join(self.patterns)}"

    def __str__(self):
        return (
            f"<Rule object {self.classe_name} ({self.classe_index}) : {self.patterns}>"
        )

    def __getstate__(self):
        # Return a dictionary containing the attributes you want to serialize

        return {
            "classe_name": self.classe_name,
            "classe_index": self.classe_index,
            "patterns": self.patterns,
            "goal": self.goal,
        }

    def __setstate__(self, state):
        # Reconstruct the object from the state dictionary
        self.classe_name = state["classe_name"]
        self.classe_index = state["classe_index"]
        self.patterns = state["patterns"]
        self.goal = state["goal"]

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

    @classmethod
    def to_yaml(cls, dumper, data):
        return dumper.represent_mapping(
            cls.yaml_tag,
            {
                "classe_name": data.classe_name,
                "classe_index": data.classe_index,
                "patterns": data.patterns,
            },
        )

    @classmethod
    def from_yaml(cls, loader, node):
        values = loader.construct_mapping(node)
        return cls(
            classe_name=values["classe_name"],
            classe_index=values["classe_index"],
            patterns=values["patterns"],
        )


class Rules:
    def __init__(self, default="Autres"):
        self.elements: list[Rule] = []
        self.default: str = default
        self.iteration = -1

    def add_rule_object(self, rule: Rule):
        self.elements.append(rule)

    def add_rule_fields(self, classe_name: str, classe_index: int, patterns: list):
        self.elements.append(
            Rule(classe_name=classe_name, classe_index=classe_index, patterns=patterns)
        )

    def add_pattern(self, class_id_or_name: str, pattern: str):
        found = False
        for ref in self.elements:
            if (
                ref.classe_index == class_id_or_name
                or ref.classe_name == class_id_or_name
            ):
                ref.add_patterns(pattern)
                found = True
        if not found:
            print("WARNING : No similar class index found !")

    def get_classname_by_id(self, class_index: int) -> str:
        for rule in self.elements:
            if rule.classe_index == class_index:
                return rule.classe_name

    def save(self, output_file: str = "rules.yaml") -> str:
        res = yaml.dump(self, Dumper=Dumper)
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
    def oldLoad(cls, file):
        dict_rules = yaml.load(file.stream, Loader=Loader)
        rules = Rules()
        for name, rule in dict_rules["categories"].items():
            rules.add_rule_object(Rule.load(name, rule))
        return rules

    @classmethod
    def load(cls, filename="rules.yaml") -> Self:
        with open(filename, "r") as f:
            stream = f.read()
        return yaml.load(stream, Loader=Loader)

    @classmethod
    def to_yaml(cls, dumper, data):
        return dumper.represent_mapping(
            cls.yaml_tag,
            {"elements": [Rule.to_yaml(dumper, rule).value for rule in data.elements]},
        )

    @classmethod
    def from_yaml(cls, loader, node):
        values = loader.construct_mapping(node)
        rules = cls()
        for rule_data in values["elements"]:
            rule_node = yaml.nodes.MappingNode(
                tag="tag:yaml.org,2002:map", value=rule_data
            )
            rules.add_rule_object(Rule.from_yaml(loader, rule_node))
        return rules

    def __getstate__(self):
        # Return a dictionary containing the attributes you want to serialize
        return {
            "elements": self.elements,
            "default": self.default,
            "iteration": self.iteration,
        }

    def __setstate__(self, state):
        # Reconstruct the object from the state dictionary
        self.elements = state["elements"]
        self.default = state["default"]
        self.iteration = state["iteration"]
