from parser import Parser
from entry import Entries, Entry
from pypdf import PdfReader
from hashlib import sha3_512
import re


class LBP_parser(Parser):
    """
    Class for the parser of type LBP_debit.
    """

    name = "LBP"

    def __init__(self):
        self.file_path = ""
        self.reader = None

    def is_line_an_expense(self, line: str) -> bool:
        """
        Determines whether or not the given line is an expense or not.
        """
        # Nothing a priori
        if re.match(r"([0-9]{2})\/([0-9]{2}).*((\d{1,3})( \d{3})*( \d{3})?,[0-9]{2})", line):
            return True
        return False

    def parse_expense_line(self, line: str) -> bool:
        """
        Given a line that have been approved by 'is_line_an_expense', parse its content into an Entry object.
        """

        print(line)
        # Price
        price = re.search(r"((\d{1,3})( \d{3})*( \d{3})?,[0-9]{2})", line).group(1)
        # price = "".join(match.group(1) for match in re.finditer('((\d{1,3})( \d{3})*( \d{3})?,[0-9]{2})', line)
        print(price, type(price), float(price.replace(' ','').replace(',','.')))
        print(line.split(price)[0])
        match = re.match(r"([0-9]{2})\/([0-9]{2})(.+)$", line.split(price)[0])
        day = match.group(1)
        month = match.group(2)
        descr = match.group(3)
        print(day, month, descr, price)
        return Entry(float(price.replace(' ','').replace(',','.')), day, month, descr)

    def preprocessing(self):
        """
        08/08ACHAT CB Kayak Bar 07.08.24 DKK 295,00 CARTE NO 526 39,54
        """
        lines = []
        pos = [m.start(0) for m in re.finditer("[0-9]{2}/[0-9]{2}[^/0-9]", self.full_text)]
        separators = ['Relevé n°', 'Totaldesopérations']
        separators_indexes = [self.full_text.index(sep) for sep in separators]
        full_separators = pos + separators_indexes
        full_separators.sort()
        for i, sep in enumerate(full_separators[:-1]):
            lines.append(self.full_text[sep:full_separators[i+1]])
        self.full_text = '\n'.join(lines)

    @classmethod
    def recognize(cls, file_path: str) -> bool:
        reader = PdfReader(file_path)
        full_text = "\n".join(page.extract_text() for page in reader.pages)
        keywords = ["labanquepostale.fr"]
        if all([kw in full_text for kw in keywords]):
            return True
        return False
