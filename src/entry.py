## Entries classes and functions
import csv

class Entry:
    def __init__(self, elements: list, *args, **kwargs):
        """
        elements : list
        price_index : index of the expense amount in the line
        day_index : index of the expense day in the line
        month_index : index of the expense month in the line
        join_indexes : index of components that need to be fusionned in the line
        """
        self.elements = elements
        self.description = ""

        self.price = (
            float(self.elements[kwargs["price_index"]])
            if "price_index" in kwargs.keys()
            else 0
        )
        self.day = (
            int(self.elements[kwargs["day_index"]])
            if "day_index" in kwargs.keys()
            else 0
        )
        self.month = (
            int(self.elements[kwargs["month_index"]])
            if "month_index" in kwargs.keys()
            else 0
        )

        if "join_indexes" in kwargs:
            i, j = kwargs["join_indexes"]
            if j <= 0:
                j = j + len(self.elements)
            buffer = []
            for k in range(i, j):
                buffer.append(self.elements[k])
            self.description = " ".join(buffer)

    def __str__(self):
        return f"<Entry object {self.description} {self.price} {self.month} {self.day}>"


class Entries:
    def __init__(self):
        self.elements = []
        self.iteration = -1

    def add_entry_object(self, entry: Entry):
        self.elements.append(entry)

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
            "Entries Object\n"
            + "\n".join(["|\t" + str(entry) for entry in self])
            + "\n-"
        )

    @classmethod
    def import_from_file(cls, filename):
        delimiter = " "
        price_index = -1
        day_index = 1
        month_index = 0
        join_indexes = (5, -1)

        with open(filename, "r") as f:
            entries = csv.reader(f, delimiter=delimiter)
            content = list(entries)
        entries = Entries()
        for line in content:
            entries.add_entry_object(
                Entry(
                    line,
                    price_index=price_index,
                    day_index=day_index,
                    month_index=month_index,
                    join_indexes=join_indexes,
                )
            )
        return entries

