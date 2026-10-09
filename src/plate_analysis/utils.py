import numpy as np


def map_measurements(
    plate_id: str, intensities: dict[str, float], plate_map: dict[str, str]
) -> list[dict[str, str | float]]:
    """
    Maps measurements to their corresponding conditions based on the plate map.

    Args:
        plate_id (str): The identifier of the plate.
        intensities (dict): keys are identifiers of wells, values are measurements.
        plate_map (dict): keys are identifiers of wells, values are identifiers of samples.

    Returns:
        list: A list of dictionaries where each dictionary contains the plate_id, well_id, condition, and measurement.
    """
    mapped_measurements = []
    for well_id, condition in plate_map.items():
        if well_id in intensities and condition is not None:
            measurement = float(intensities[well_id])
            mapped_measurements.append(
                {
                    "plate_id": plate_id,
                    "well_id": well_id,
                    "condition": condition,
                    "measurement": measurement,
                }
            )
    return mapped_measurements


def select_wells(
    measurements: list[dict[str, str | float]], source: dict[str, list[str]]
) -> list[dict[str, str | float]]:
    """
    Selects measurements that match the specified conditions for a given source.

    Args:
        measurements (list): A list of dictionaries where each dictionary contains the plate_id, well_id, condition, and measurement.
        source (dict): A dictionary where keys are plate IDs and values are lists of conditions to select.

    Returns:
        list: A list of dictionaries containing only the measurements that match the specified conditions.
    """
    selected_measurements = []
    for measurement in measurements:
        plate_id = measurement["plate_id"]
        condition = measurement["condition"]
        if plate_id in source and condition in source[plate_id]:
            selected_measurements.append(measurement)
    return selected_measurements


def group_by_condition(data: list[dict[str, str | float]]) -> dict[str, list[float]]:
    """
    Groups measurements by condition.

    Args:
        data (list): A list of dictionaries where each dictionary contains the plate_id, well_id, condition, and measurement.

    Returns:
        dict: keys are identifiers of conditions, values are lists of measurements.
    """
    result = {}
    for entry in data:
        condition = entry["condition"]
        measurement = entry["measurement"]
        if condition in result:
            result[condition].append(measurement)
        else:
            result[condition] = [measurement]
    return result


def normalise_to_min_max(data: dict[str, list[float]]) -> dict[str, list[float]]:
    """
    Normalises the data to the range [0, 1] based on the minimum and maximum values.

    Args:
        data (dict): keys are identifiers of samples, values are lists of measurements.
    """
    all_values = [value for values in data.values() for value in values]
    min_value = min(all_values)
    max_value = max(all_values)

    normalised_data = {}
    for condition, values in data.items():
        normalised_data[condition] = [
            (value - min_value) / (max_value - min_value) for value in values
        ]

    return normalised_data


def normalise_to_controls(
    data: dict[str, list[float]],
    positive_control: str,
    negative_control: str,
) -> dict[str, list[float]]:

    pc = np.nanmedian(data[positive_control])
    nc = np.nanmedian(data[negative_control])

    if not np.isfinite(pc) or not np.isfinite(nc):
        raise ValueError("Control medians must be finite.")

    if pc >= nc:
        raise ValueError(
            "Expected positive control to have lower "
            "chemiluminescence than negative control."
        )

    return {
        condition: [float((value - pc) / (nc - pc)) for value in values]
        for condition, values in data.items()
    }
