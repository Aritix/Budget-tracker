from src.data_processing.parser import Parser
from src.data_processing.entry import Entries, Entry
from pypdf import PdfReader
from werkzeug.datastructures import FileStorage
import re

class BNC_MasterCard_parser(Parser):
    """
    Class for the parser of type BNC_MasterCard.
    """
    name = 'BNC_MasterCard'

    def __init__(self):
        self.file_path = ""
        self.reader = None
        
    def is_line_an_expense(self, line: str) -> bool:
        """
        Determines whether or not the given line is an expense or not.
        """
        # Number of spaces check
        # if "WATER" in line:
        print(line)
        if line.count(" ") >= 2:
            # Price format check
            price = line.split(" ")[-1]
            if price.count(".") == 1:
                decimals = price.split(".")[1]
                # print(line, price, decimals)
                if (len(decimals) == 2 and decimals.isdigit()) or (
                    len(decimals) == 3 and decimals[:2].isdigit() and decimals[2] == "-"
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
        print(line)
        m1 = line[:2]
        d1 = line[2:4]
        ref = line[4:14]
        descr = " ".join(line[18:].split(" ")[:-1])
        amount_str = line.split(" ")[-1]
        amount = -float(amount_str[:-1]) if '-' in amount_str else float(amount_str)
        return Entry(price=amount, day=d1, month=m1, description=descr)

    def preprocessing(self) -> None:
        """
        Modify the full_text attribute before passing parsing the lines
        """
        self.full_text = self.full_text.replace('\nMONTANTORIGINALENDEVISE', ' DEVISE ')

    @classmethod
    def recognize(cls, file: FileStorage) -> bool:
        reader = PdfReader(file.stream)
        full_text = "\n".join(page.extract_text() for page in reader.pages)
        keywords = ["MASTERCARD SOLUTIONS", "National Bank"]
        if all([kw in full_text for kw in keywords]):
            return True
        return False