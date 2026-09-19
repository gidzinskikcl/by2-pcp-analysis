import pathlib

def read_plate_map(file_path: pathlib.Path) -> dict[str, str]:
    """
    Reads a plate map from a CSV file and returns it as a dictionary.

    Args:
        file_path (str): The path to CSV plate map.

    Returns:
        dict: keys are identifiers of wells, values are identifiers of samples.
    """

class InvalidPlateMapError(ValueError):
    """
    Raised when a plate map is invalid.
    """
