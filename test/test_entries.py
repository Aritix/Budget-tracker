# from src.entry import Entry
from src.data_processing.entry import Entry, Entries

TEST_DIR = "test/"
TEST_DATA_DIR = f"data/test/"
TEST_ENTRY_PATH = f"{TEST_DATA_DIR}entry_test.txt"


def test_import_entries_on_file():

    entries = Entries.import_from_file(TEST_ENTRY_PATH)
    assert len(entries.elements) == 10
    assert entries.elements[0].day == "01"
    assert entries.elements[0].month == "01"
    assert entries.elements[0].description == "FOOD"
    assert entries.elements[0].price == 10.5

def test_add_entry_object():
    entries = Entries()
    assert len(entries.elements) == 0
    entry_1 = Entry()
    entries.add_entry_object(entry_1)
    assert len(entries.elements) == 1
    assert entries.elements[0] == entry_1
    entry_2 = Entry(price=100.48, day='31', month='12', description='category')
    entries.add_entry_object(entry_2)
    assert len(entries.elements) == 2
    assert entries.elements[1] == entry_2

def test_iterate_on_entries():
    entries = Entries.import_from_file(TEST_ENTRY_PATH)

    reference = [
        ["01", "01", "FOOD", 10.5],
        ["01", "02", "CLOTHES", 60.0],
        ["01", "03", "GROCERIES", 20.0],
        ["01", "04", "FOOD", 20.0],
        ["01", "05", "HOME", 50.0],
        ["01", "06", "AMAZON", 40.0],
        ["01", "07", "GROCERIES", 30.0],
        ["01", "07", "GROCERIES", 30.0],
        ["01", "09", "BUS", 5.0],
        ["01", "10", "FOOD", 25.0],
    ]
    res = []
    for entry in entries:
        res_line=[]
        res_line.append(entry.month)
        res_line.append(entry.day)
        res_line.append(entry.description)
        res_line.append(entry.price)
        res.append(res_line)
    assert len(reference) == len(res)
    assert reference == res
