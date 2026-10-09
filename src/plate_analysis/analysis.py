from plate_analysis import plate_map, fiji, plot, utils, entities


def analyse_run(
    run: entities.RunConfig,
) -> list[tuple[entities.ExperimentConfig, dict[str, list[float]]]]:

    plate_maps = plate_map.read_plate_maps(file_path=run.plate_map_path)

    measurements = []

    for plate in run.plates:
        intensities = fiji.read_fiji_results(file_path=plate.intensities_path)

        plate_measurements = utils.map_measurements(
            plate_id=plate.plate_id,
            intensities=intensities,
            plate_map=plate_maps[plate.plate_id],
        )

        measurements.extend(plate_measurements)

    experiments_data = []

    for experiment in run.experiments:
        selected = utils.select_wells(
            measurements=measurements,
            source=experiment.source,
        )

        grouped = utils.group_by_condition(data=selected)

        labelled = {
            experiment.labels[condition]: values
            for condition, values in grouped.items()
        }

        if experiment.normalisation == "controls":
            if experiment.negative_control is None:
                raise ValueError(
                    f"{experiment.name}: control normalisation "
                    "requires a negative control."
                )

            normalised = utils.normalise_to_controls(
                data=labelled,
                positive_control=experiment.positive_control,
                negative_control=experiment.negative_control,
            )

        elif experiment.normalisation == "minmax":
            normalised = utils.normalise_to_min_max(data=labelled)

        else:
            raise ValueError(f"Unknown normalisation: {experiment.normalisation}")

        experiments_data.append((experiment, normalised))

    return experiments_data
