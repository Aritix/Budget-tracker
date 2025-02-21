"""
Definition de la classe abstraite de parser et de l'algorithme d'identification de type de fichier pdf.
"""
from pypdf import PdfReader
from entry import Entry, Entries



class Parser:

    def __init__(self):
        self.file_path = ""
        self.reader = None

    def load(self, file_path):
        """
        Load the statement file.
        """
        self.file_path = file_path
        self.reader = PdfReader(file_path)
        self.full_text = "\n".join(page.extract_text() for page in self.reader.pages)

    def transform_to_entries(self) -> Entries:
        """
        Parse the loaded file to an Entries object
        """
        assert self.file_path != ''
        self.preprocessing()
        lines = self.full_text.split("\n")
        entries = Entries()
        for line in lines:
            if self.is_line_an_expense(line):
                entries.add_entry_object(self.parse_expense_line(line))
        return entries

    def preprocessing(self):
        """
        Modify the full_text attribute before passing parsing the lines
        """
        ...

    def is_line_an_expense(self, line: str) -> bool:
        """
        Determines whether or not the given line is an expense or not.
        """
        ...

    def parse_expense_line(self, line: str) -> bool:
        """
        Given a line that have been approved by 'is_line_an_expense', parse its content into an Entry object.
        """
        ...
    @classmethod
    def recognize(cls, file_path: str) -> bool:
        ...