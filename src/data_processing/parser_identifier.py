from src.data_processing.BNC_MasterCard_parser import BNC_MasterCard_parser
from src.data_processing.BNC_debit_parser import BNC_debit_parser
from src.data_processing.LBP_parser import LBP_parser
from werkzeug.datastructures import FileStorage
from src.data_processing.parser import Parser
def parser_identifier(file: FileStorage) -> Parser:
    parser_types = [BNC_MasterCard_parser, BNC_debit_parser, LBP_parser]
    for parser_type in parser_types:
        if parser_type.recognize(file):
            print(f"Found type : {parser_type.name} for {file.filename}")
            return parser_type()
    print(f"No parser found for {file.filename}")