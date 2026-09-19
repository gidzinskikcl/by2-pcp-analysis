from src.plate_analysis import plate_map
def test_read_plate_map():
    plate_map = plate_map.read_plate_map("tests/data/plate_map.csv")

    assert len(plate_map) == 60
    assert plate_map["B2"] == "Rx+CP"
    assert plate_map["B3"] == "Rx+CP"
    assert plate_map["C5"] == "CAN113+SRE2"

def test_missing_plate_id():
    # Excel has no Plate X
    pass

def test_missing_well():
    # e.g. D7 is blank
    pass


def test_used_outer_well():
    # e.g. A5 contains "Rx+CP"
    pass

