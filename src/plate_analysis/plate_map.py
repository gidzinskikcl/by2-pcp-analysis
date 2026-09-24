import re
import pathlib
from openpyxl import load_workbook

class InvalidPlateMapError(ValueError):
    """
    Raised when a plate map is invalid.
    """

BLANK_WELLS = [
    "A1", "A2", "A3", "A4", "A5", "A6", "A7", "A8", "A9", "A10", "A11", "A12",
    "B1", "B12",
    "C1", "C12",
    "D1", "D12",
    "E1", "E12",
    "F1", "F12",
    "G1", "G12",
    "H1", "H2", "H3", "H4", "H5", "H6", "H7", "H8", "H9", "H10", "H11", "H12"
]

def read_plate_maps(file_path: pathlib.Path) -> dict[str, dict[str, str]]:
    """
    Reads a 96-well plate map(s) from a CSV file and returns it as a dictionary.

    Args:
        file_path (str): The path to CSV plate map.

    Returns:
        dict: A dictionary where keys are plate ids and values are dictionaries mapping well ids to sample ids.
    """
    wb = load_workbook(file_path, data_only=True)
    ws = wb.active

    result = {}

    plates = _find_plates(ws=ws)

    for plate_id, grid in plates.items():
        for i in range(12): # 12 columns
            for j in range(8): # 8 rows
                well_id = f"{chr(ord('A') + j)}{i + 1}"
                sample = ws.cell(row=grid[0] + j, column=grid[1] + i).value

                # Checl for blank wells
                if (sample is None) and (well_id not in BLANK_WELLS):
                    raise InvalidPlateMapError(f"{well_id} is blank in plate {plate_id}.")
                # Check for used outer wells
                elif (sample is not None) and (well_id in BLANK_WELLS):
                    raise InvalidPlateMapError(f"{well_id} is used in plate {plate_id}")
                
                if plate_id not in result:
                    result[plate_id] = {}
                result[plate_id][well_id] = sample

    return result


def _find_plates(ws: object) -> dict[str, tuple[int, int]]:
    """
    Finds all plate ids in the given worksheet.

    Args:
        ws (openpyxl.worksheet.worksheet.Worksheet): The worksheet to search for plate ids.

    Returns:
        dict: A dictionary where keys are plate ids and values are tuples of (row, column) coordinates of the plate id cell.
    """
    result = {}
    plate_pattern = re.compile(r"Plate\s+(\d+)$", re.IGNORECASE)
    # "Plate" * whitespace+ * [1-9][0-9]*
    # Plate\s+(\d+)$
    # │     │   │   │
    # │     │   │   └─ end of string
    # │     │   └───── one or more digits
    # │     └───────── one or more whitespaces
    # └─────────────── "Plate"
    for row in ws.iter_rows():
        for cell in row:
            match = plate_pattern.match(str(cell.value).strip())
            if match:
                plate_id = match.group(1)
                result[plate_id] = (cell.row+1, cell.column+1)
    if not result:
        raise InvalidPlateMapError("No plate ids found in the worksheet.")
    return result





def show_plate_map(plate_map: dict[str, str], id=0) -> None:
    """
    Displays a plate map in a human-readable format.

    Args:
        plate_map (dict): keys are identifiers of wells, values are identifiers of samples.
    """
    if id != 0:
        print(f"Plate Map {id}:")
    else:
        print("Plate Map:")
    for row_letter in "ABCDEFGH":
        row_values = []
        for well_number in range(1, 13):
            well_id = f"{row_letter}{well_number}"
            sample = plate_map.get(well_id, "")
            row_values.append(sample if sample is not None else "")
        print(f"{row_letter}: {', '.join(row_values)}")
