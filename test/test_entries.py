# from src.entry import Entry
from src.entry import Entry, Entries
TEST_DIR = "test/"
TEST_DATA_DIR = f"{TEST_DIR}test_data/"
TEST_ENTRY_PATH = f"{TEST_DATA_DIR}entry_test.txt"

def test_entries_on_file():
    
    entries = Entries.import_from_file(TEST_ENTRY_PATH)
    assert len(entries.elements) == 10
    assert entries.elements[0].day == "01"
    assert entries.elements[0].month == "01"
    assert entries.elements[0].description == "FOOD"
    assert entries.elements[0].price == 10.5