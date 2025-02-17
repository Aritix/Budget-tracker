## Entries classes and functions
import csv


class Entry:
    def __init__(self, price=0, day="00", month="00", description=""):
        self.price = price
        self.day = day
        self.month = month
        self.description = description

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
        descr_index = 5

        with open(filename, "r") as f:
            entries = csv.reader(f, delimiter=delimiter)
            content = list(entries)
        entries = Entries()
        for line in content:
            entries.add_entry_object(
                Entry(
                    price=float(line[price_index]),
                    day=line[day_index],
                    month=line[month_index],
                    description=line[descr_index],
                )
            )
        return entries
