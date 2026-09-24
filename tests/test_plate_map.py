import pytest

from openpyxl import Workbook
from src.plate_analysis import plate_map

def test_read_single_plate_map(tmp_path):

    maps = plate_map.read_plate_maps("tests/data/PCP_single_test.xlsx")


    len(maps) == 1
    assert "3" in maps
    result = maps["3"]
    assert len(result) == 96
    assert result["B2"] == "Rx+CP"
    assert result["C3"] == "CAN113+PTO"
    assert result["D4"] == "CAN113+PTO"
    assert result["E5"] == "CAN113+PTO"
    assert result["F6"] == "CAN113+CP"
    assert result["G7"] == "CAN113+CP"
    assert result["B8"] == "CAN113+CP"
    assert result["C9"] == "CAN113"
    assert result["D10"] == "CAN113"
    assert result["E11"] == "CAN113"

def test_read_multi_plate_map(tmp_path):

    maps = plate_map.read_plate_maps("tests/data/PCP_multi_test.xlsx")

    len(maps) == 3

    assert "1" in maps
    assert "11" in maps
    assert "4" in maps

    result_1 = maps["1"]
    result_11 = maps["11"]
    result_4 = maps["4"]

    assert len(result_1) == 96
    assert len(result_11) == 96
    assert len(result_4) == 96

    assert result_1["B2"] == "Sr35WT + AvrS35"
    assert result_11["B2"] == "Sr35WT + AvrS35"
    assert result_4["B2"] == "Sr35WT + AvrS35"


    assert result_1["E5"] == "Sr35-52 + AvrS35"
    assert result_11["E5"] == "Sr35-59 + AvrS35"
    assert result_4["E5"] == "Sr35-59 + AvrS35"

    assert result_1["D10"] == " Sr35-52 + SRE2"
    assert result_11["D10"] == " Sr35-59 + SRE2"
    assert result_4["D10"] == " Sr35-59 + SRE2"


def test_missing_plate_id():
    # Excel has no Plate X
    with pytest.raises(plate_map.InvalidPlateMapError):
        results = plate_map.read_plate_maps("tests/data/PCP_noPlate_test.xlsx")  



def test_missing_well():
    # e.g. D7 is blank
    with pytest.raises(plate_map.InvalidPlateMapError):
        results = plate_map.read_plate_maps("tests/data/PCP_blankWell_test.xlsx")


def test_used_outer_well():
    # e.g. A5 contains "Rx+CP"
     with pytest.raises(plate_map.InvalidPlateMapError):
        results = plate_map.read_plate_maps("tests/data/PCP_outerWell_test.xlsx")

# def test_show_plate_map():
#     maps = plate_map.read_plate_maps("tests/data/PCP_single_test.xlsx")
#     plate = maps["3"]
#     plate_map.show_plate_map(plate_map=plate, id=3)
#     assert 1 == 0
