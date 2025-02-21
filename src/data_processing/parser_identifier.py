from BNC_MasterCard_parser import BNC_MasterCard_parser
from BNC_debit_parser import BNC_debit_parser
from LBP_parser import LBP_parser

def parser_identifier(file_path: str):
    parser_types = [BNC_MasterCard_parser, BNC_debit_parser, LBP_parser]
    for parser_type in parser_types:
        if parser_type.recognize(file_path):
            print(f"Found type : {parser_type.name} for {file_path}")
            return parser_type()
    print(f"No parser found for {file_path}")