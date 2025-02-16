from pypdf import PdfReader
from entry import Entry, Entries


class BNC_MasterCard_parser:
    """
    Class for the parser of type BNC_MasterCard.
    """

    def __init__(self):
        self.file_path = ""
        self.reader = None

    def load(self, file_path):
        """
        Load the statement file.
        """
        self.file_path = file_path
        self.reader = PdfReader(file_path)

    def transform_to_entries(self) -> Entries:
        """
        Parse the loaded file to an Entries object
        """
        assert self.file_path != ''
        full_text = "\n".join(page.extract_text() for page in self.reader.pages)
        lines = full_text.split("\n")
        entries = Entries()
        for line in lines:
            if self.is_line_an_expense(line):
                entries.add_entry_object(self.parse_expense_line(line))
        return entries

    def is_line_an_expense(self, line: str) -> bool:
        """
        Determines whether or not the given line is an expense or not.
        """
        # Number of spaces check
        if line.count(" ") >= 2:
            # Price format check
            price = line.split(" ")[-1]
            if price.count(".") == 1:
                decimals = price.split(".")[1]
                if (len(decimals) == 2 and decimals.isdigit()) or (
                    len(decimals) == 3 and decimals[:2].isdigit() and decimals[3] == "-"
                ):
                    # Dates format check
                    month, day = line[:2], line[2:4]
                    if (
                        day.isdigit()
                        and month.isdigit()
                        and int(month) in range(1, 13)
                        and int(day) in range(1, 32)
                    ):
                        # Reference number format checks
                        ref = line[5:15]
                        if ref[1:].isdigit() and ref[0].isalpha:
                            return True
        return False

    def parse_expense_line(self, line: str) -> bool:
        """
        Given a line that have been approved by 'is_line_an_expense', parse its content into an Entry object.
        """
        m1 = line[:2]
        d1 = line[2:4]
        ref = line[4:14]
        descr = " ".join(line[18:].split(" ")[:-1])
        amount = line.split(" ")[-1]
        return Entry([d1, m1, descr, amount], price_index=3, day_index=0, month_index=1, descr_index=2)
