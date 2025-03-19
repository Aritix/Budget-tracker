from src.data_processing.parser import Parser
from src.data_processing.entry import Entries, Entry
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

        # Price
        print(line)
        currency = "EUR"
        price_pattern = r" ((\d{1,3})( \d{3})*( \d{3})?,[0-9]{2})"
        price = re.search(price_pattern, line).group(1)
        if len(re.findall(price_pattern, line)) == 1:
            currency = "EUR"
        elif len(re.findall(r" [A-Z]{3} "+price, line)) > 0:
            # Parse the currency
            i = line.index(price)
            currency = line[i-4:i-1]
        
        # Knowing whether an entry is an income or an outcome is not easy with this format
        incomes_indicators = ["VIREMENT DE"]
        sign = 1
        for indicator in incomes_indicators:
            if indicator in line:
                sign = -1

        match = re.match(r"([0-9]{2})\/([0-9]{2})(.+)$", line.split(price)[0])
        day = match.group(1)
        match = re.match(r"([0-9]{2})\/([0-9]{2})(.+)$", line.split(price)[0])
        day = match.group(1)
        month = match.group(2)
        descr = match.group(3)
        print(Entry(sign*float(price.replace(' ','').replace(',','.')), day, month, descr, currency=currency))
        return Entry(sign*float(price.replace(' ','').replace(',','.')), day, month, descr, currency=currency)

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
