import pytest

from src.plate_analysis import grouping

@pytest.fixture
def plate_map():
    result = {
        "A1": "Condition1", "A2": "Condition1", "A3": "Condition1",
        "A4": "Condition2", "A5": "Condition2", "A6": "Condition2",
        "A7": "Condition3", "A8": "Condition3", "A9": "Condition3",
        "A10": "Condition4", "A11": "Condition4", "A12": "Condition4",

        "B1": "Condition1", "B2": "Condition1", "B3": "Condition1",
        "B4": "Condition2", "B5": "Condition2", "B6": "Condition2",
        "B7": "Condition3", "B8": "Condition3", "B9": "Condition3",
        "B10": "Condition4", "B11": "Condition4", "B12": "Condition4",

        "C1": "Condition1", "C2": "Condition1", "C3": "Condition1",
        "C4": "Condition2", "C5": "Condition2", "C6": "Condition2",
        "C7": "Condition3", "C8": "Condition3", "C9": "Condition3",
        "C10": "Condition4", "C11": "Condition4", "C12": "Condition4",

        "D1": "Condition1", "D2": "Condition1", "D3": "Condition1",
        "D4": "Condition2", "D5": "Condition2", "D6": "Condition2",
        "D7": "Condition3", "D8": "Condition3", "D9": "Condition3",
        "D10": "Condition4", "D11": "Condition4", "D12": "Condition4",

        "E1": "Condition1", "E2": "Condition1", "E3": "Condition1",
        "E4": "Condition2", "E5": "Condition2", "E6": "Condition2",
        "E7": "Condition3", "E8": "Condition3", "E9": "Condition3",
        "E10": "Condition4", "E11": "Condition4", "E12": "Condition4",

        "F1": "Condition1", "F2": "Condition1", "F3": "Condition1",
        "F4": "Condition2", "F5": "Condition2", "F6": "Condition2",
        "F7": "Condition3", "F8": "Condition3", "F9": "Condition3",
        "F10": "Condition4", "F11": "Condition4", "F12": "Condition4",

        "G1": "Condition1", "G2": "Condition1", "G3": "Condition1",
        "G4": "Condition2", "G5": "Condition2", "G6": "Condition2",
        "G7": "Condition3", "G8": "Condition3", "G9": "Condition3",
        "G10": "Condition4", "G11": "Condition4", "G12": "Condition4",

        "H1": "Condition1", "H2": "Condition1", "H3": "Condition1",
        "H4": "Condition2", "H5": "Condition2", "H6": "Condition2",
        "H7": "Condition3", "H8": "Condition3", "H9": "Condition3",
        "H10": "Condition4", "H11": "Condition4", "H12": "Condition4",
    }

    return result

@pytest.fixture
def intensities():
    return {
        f"{row}{col}": str(100 + i * 10)
        for i, (row, col) in enumerate(
            (row, col)
            for row in "ABCDEFGH"
            for col in range(1, 13)
        )
    }

@pytest.fixture
def expected() -> dict[str, list[float]]:
    return {
        "Condition1": [
            100.0, 110.0, 120.0,
            220.0, 230.0, 240.0,
            340.0, 350.0, 360.0,
            460.0, 470.0, 480.0,
            580.0, 590.0, 600.0,
            700.0, 710.0, 720.0,
            820.0, 830.0, 840.0,
            940.0, 950.0, 960.0,
        ],
        "Condition2": [
            130.0, 140.0, 150.0,
            250.0, 260.0, 270.0,
            370.0, 380.0, 390.0,
            490.0, 500.0, 510.0,
            610.0, 620.0, 630.0,
            730.0, 740.0, 750.0,
            850.0, 860.0, 870.0,
            970.0, 980.0, 990.0,
        ],
        "Condition3": [
            160.0, 170.0, 180.0,
            280.0, 290.0, 300.0,
            400.0, 410.0, 420.0,
            520.0, 530.0, 540.0,
            640.0, 650.0, 660.0,
            760.0, 770.0, 780.0,
            880.0, 890.0, 900.0,
            1000.0, 1010.0, 1020.0,
        ],
        "Condition4": [
            190.0, 200.0, 210.0,
            310.0, 320.0, 330.0,
            430.0, 440.0, 450.0,
            550.0, 560.0, 570.0,
            670.0, 680.0, 690.0,
            790.0, 800.0, 810.0,
            910.0, 920.0, 930.0,
            1030.0, 1040.0, 1050.0,
        ],
    }


def test_group_by_condition(plate_map, intensities, expected):
    observed = grouping.group_by_condition(intensities, plate_map)
    assert observed == expected