## Entries classes and functions
import csv
import base64
from typing import Self 


class Entry:
    """
    Object representing a transaction (expense or income) with a context.
    """
    delimiter = "¬"
    def __init__(self, price=0, day="00", month="00", description="", category=None, currency="CAD"):
        self.price = price
        self.day = day
        self.month = month
        self.description = description
        self.category = category
        self.currency = currency

    def save(self, filename=None, tostring=True) -> str | None:
        """
        Save the *Entry* objects as a JSON string. Can be later loaded by the *load* class method.
        """
        res = base64.b64encode(
            f"{self.price}{Entry.delimiter}{self.day}{Entry.delimiter}{self.month}{Entry.delimiter}{self.description}{Entry.delimiter}{self.category if self.category else "None"}".encode()
        )
        if tostring:
            return res.decode()
        if filename:
            with open(filename, "w") as f:
                f.write(res)
        return res

    @classmethod
    def load(cls, data: str) -> Self:
        """
        Load an *Entry* object saved with the *save* method.
        """
        data = base64.b64decode(data).decode()
        data = data.split(cls.delimiter)
        return cls(
            price=float(data[0]), day=data[1], month=data[2], description=data[3], category=data[4] if data[4] != "None" else None
        )



    def __str__(self):
        return f"<Entry object {self.description} {self.price} {self.month} {self.day} {self.category}>"


class Entries:
    """
    Collection of entries.
    """
    def __init__(self):
        self.elements = []
        self.iteration = -1

    def add_entry_object(self, entry: Entry):
        self.elements.append(entry)
    
    def add_entries(self, entries: list[Entry]):
        for entry in entries:
            self.add_entry_object(entry)

    def __len__(self):
        return len(self.elements)

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

    def save(self, filename=None, tostring=True) -> str | None:
        """
        Save the *Entries* objects as a JSON string. Can be later loaded by the *load* class method.
        """
        res = ""
        for entry in self:
            res += entry.save(tostring=True) + " "
        if tostring:
            return res
        if filename:
            with open(filename, "w") as f:
                f.write(res)
        return res

    @classmethod
    def load(cls, data: str) -> Self:
        """
        Load an *Entries* object saved with the *save* method.
        """
        data = data.split(" ")
        entries = Entries()
        for entry in data:
            entries.add_entry_object(Entry.load(entry))
        return entries
    


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
