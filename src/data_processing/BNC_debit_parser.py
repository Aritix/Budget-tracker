from src.data_processing.parser import Parser
from src.data_processing.entry import Entries, Entry
from pypdf import PdfReader
from hashlib import sha3_512
import re


class BNC_debit_parser(Parser):
    """
    Class for the parser of type BNC_debit.
    """

    name = "BNC_debit"

    def __init__(self):
        self.file_path = ""
        self.reader = None

    def is_line_an_expense(self, line: str) -> bool:
        """
        Determines whether or not the given line is an expense or not.
        """
        line = line.strip()
        # print(line)
        # Number of spaces check
        if line.count(" ") > 6:
            # Day and Month format check
            day = line.split(" ")[0]
            month = line.split(" ")[1]
            if (
                len(day) == 2
                and day.isdigit()
                and len(month) == 3
                and month
                in [
                    "JAN",
                    "FEV",
                    "MAR",
                    "AVR",
                    "MAI",
                    "JUI",
                    "JUI",
                    "AOU",
                    "SEP",
                    "OCT",
                    "NOV",
                    "DEC",
                ]
            ):
                return True
        return False

    def parse_expense_line(self, line: str) -> bool:
        """
        Given a line that have been approved by 'is_line_an_expense', parse its content into an Entry object.
        """
        ...

        line = line.strip()
        day = line.split(" ")[0]
        month = line.split(" ")[1]
        month = {
            "JAN": "01",
            "FEV": "02",
            "MAR": "03",
            "AVR": "04",
            "MAI": "05",
            "JUI": "06",
            "JUI": "07",
            "AOU": "08",
            "SEP": "09",
            "OCT": "10",
            "NOV": "11",
            "DEC": "12",
        }[month]
        price = line.split("           ")[1].replace(",", ".").replace(' ', '')
        if line[-1] == '-':
            price = '-'+price[:-1]
        price = float(price)
        # descr = ' '.join(line.replace(' ', '').split()[2:-2])
        descr = line[7:line.index('   ')]
        # print(f"{day}, {month}, {price}, #{descr}#")
        # input()

        return Entry(price, day, month, descr)

    def preprocessing(self):
        res = []
        last_total = float(re.search(r"""SOLDE PRECEDENT\n\s{5,15}([0-9 ]+,[0-9]{2})""", self.full_text).group(1).replace(' ', '').replace(',','.'))
        for i, line in enumerate(
            self.full_text.split(
                "................................................................................................................................................................................................................."
            )
        ):
            if i == 0:
                res.append(line)
            else:
                # Check if the amount is received or spent
                now_total = line.split("   ")[-1].replace(' ', '').replace(',','.')
                try: # Received
                    now_total = float(now_total)
                    if now_total > last_total:
                        line += '-'
                except ValueError: # Spent
                    pass
                last_total = now_total
                if "Suite en page" in line:
                    res.append(line.replace("\n", " ").split("Suite en page")[0])
                elif "Total" in line:
                    res.append(line.replace("\n", " ").split("Total")[0])
                else:
                    res.append(line.replace("\n", " "))
        open("pre.txt", "w").write(self.full_text)
        open("post.txt", "w").write("\n".join(res))
        self.full_text = "\n".join(res)

    @classmethod
    def recognize(cls, file_path: str) -> bool:
        reader = PdfReader(file_path)
        full_text = "\n".join(page.extract_text() for page in reader.pages)
        keywords = ["BANQUE NATIONALE DU CANADA"]
        images = sum([list(page.images) for page in reader.pages], [])
        hashes = [sha3_512(image.data).hexdigest() for image in images]
        hash_ref = [
            "886f17b956ce9c033fe0519d47db3deca6428902a2830ab3e08e132119f4635249268250ad8367fd2b22c20ef4132d3178ca26f12ae08e8eebc6e90bfa581e68",
            "f18653a5ce9cbac0ae9d1389b923c6cb28b2d7e2696b0ae2bf73fdde09e1404f34014bd9665bafe408d54cac64eb42bdbac77179d7119b128882827351058866",
        ]
        if all([hr in hashes for hr in hash_ref]) and all(
            [kw in full_text for kw in keywords]
        ):
            return True
        return False
