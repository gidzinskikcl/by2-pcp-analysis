import pathlib

def read_fiji_results(file_path: pathlib.Path) -> dict[str, float]:
    """
    Reads Fiji results from a CSV file and returns it as a dictionary.

    Args:
        file_path (str): The path to CSV Fiji results.
    
    Returns:
        dict: keys are identifiers of wells, values are measurements.
    """