import pathlib

def read_fiji_results(file_path: pathlib.Path) -> dict[str, float]:
    """
    Reads Fiji results from a CSV file and returns it as a dictionary.

    Args:
        file_path (str): The path to CSV Fiji results.
    
    Returns:
        dict: keys are identifiers of wells, values are measurements.
    """
    result = {}
    with open(file_path, "r") as f:
        lines = f.readlines()
        for line in lines[1:]: # Skip the header
            parts = line.strip().split(",")
            well_id = parts[1]
            intensity = float(parts[2]) if parts[2] != "NaN" else float("nan")
            result[well_id] = intensity

    return result