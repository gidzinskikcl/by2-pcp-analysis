def group_by_condition(
        intensities: dict[str, float],
        plate_map: dict[str, str]
) -> dict[str, list[float]]:
    """
    Groups intensities by condition based on the plate map.

    Args:
        intensities (dict): keys are identifiers of wells, values are measurements.
        plate_map (dict): keys are identifiers of wells, values are identifiers of samples.

    Returns:
        dict: keys are identifiers of samples, values are lists of measurements.
    """