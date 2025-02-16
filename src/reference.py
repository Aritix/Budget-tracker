## References classes and functions
import csv

class Reference:
    def __init__(self, classe_name: str, classe_index: int, patterns: list):
        self.classe_name = classe_name
        self.classe_index = classe_index
        self.patterns = patterns

    def __str__(self):
        return f"<Reference object {self.classe_name} ({self.classe_index}) : {self.patterns}>"

    @classmethod
    def ref_from_list(cls, reference_list):
        class_name_index = 0
        classe_index = 1
        patterns_index = 2
        return Reference(
            classe_name=reference_list[class_name_index],
            classe_index=reference_list[classe_index],
            patterns=reference_list[patterns_index].split(","),
        )


class References:
    def __init__(self):
        self.elements = []
        self.iteration = -1

    def add_ref_object(self, reference: Reference):
        self.elements.append(reference)

    def add_ref_fields(self, classe_name: str, classe_index: int, patterns: list):
        self.elements.append(
            Reference(
                classe_name=classe_name, classe_index=classe_index, patterns=patterns
            )
        )

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
        return (
            "References Object\n"
            + "\n".join(["|\t" + str(ref) for ref in self])
            + "\n-"
        )

    @classmethod
    def import_from_file(cls, filename):
        delimiter = "|"
        with open(filename, "r") as f:
            references = csv.reader(f, delimiter=delimiter)
            content = list(references)
        references = References()
        for line in content:
            references.add_ref_object(Reference.ref_from_list(line))
        return references
