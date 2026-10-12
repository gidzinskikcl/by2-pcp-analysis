from plate_analysis import plate_map, fiji, statistics, utils, entities


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


def analyse_statistics(
    experiments_data: list[tuple[entities.ExperimentConfig, dict[str, list[float]]]],
):
    results = {}

    for experiment, data in experiments_data:

        descriptive = statistics.descriptive_stats(data)
        comparisons = {}
        candidate_comparisons = {}

        has_negative = experiment.negative_control is not None
        has_specificity = experiment.specificity_control is not None

        if has_negative or has_specificity:

            for condition in experiment.experimental_conditions:
                comparisons[condition] = {}

                if has_negative:
                    comparisons[condition]["negative_control"] = (
                        statistics.compare_conditions(
                            data[condition],
                            data[experiment.negative_control],
                        )
                    )

                if has_specificity:
                    comparisons[condition]["specificity_control"] = (
                        statistics.compare_conditions(
                            data[condition],
                            data[experiment.specificity_control],
                        )
                    )

        else:
            candidate_comparisons = statistics.compare_candidates(
                data=data,
                candidates=experiment.experimental_conditions,
            )

        results[experiment.name] = {
            "descriptive": descriptive,
            "comparisons": comparisons,
            "candidate_comparisons": candidate_comparisons,
        }

    return results


def apply_bh_correction(
    statistical_results: dict,
    alpha: float = 0.05,
) -> None:

    # Separate families of comparisons
    for control_type in ("negative_control", "specificity_control"):

        comparisons = []

        for experiment_result in statistical_results.values():
            for condition_result in experiment_result["comparisons"].values():

                if control_type in condition_result:
                    comparisons.append(condition_result[control_type])

        if not comparisons:
            continue

        p_values = [comparison["p_value"] for comparison in comparisons]

        adjusted, significant = statistics.adjust_p_values(
            p_values,
            alpha=alpha,
        )

        for comparison, p_adj, is_significant in zip(
            comparisons, adjusted, significant
        ):
            comparison["adjusted_p_value"] = p_adj
            comparison["significant"] = is_significant

    # Correct candidate-to-candidate comparisons
    for experiment_result in statistical_results.values():

        candidate_comparisons = experiment_result["candidate_comparisons"]

        if not candidate_comparisons:
            continue

        comparisons = list(candidate_comparisons.values())

        adjusted, significant = statistics.adjust_p_values(
            [comparison["p_value"] for comparison in comparisons],
            alpha=alpha,
        )

        for comparison, p_adj, is_significant in zip(
            comparisons, adjusted, significant
        ):
            comparison["adjusted_p_value"] = p_adj
            comparison["significant"] = is_significant
