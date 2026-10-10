from experiments.inf_1209 import RUN_1209
from plate_analysis import analysis, plot


def main():

    RUNS = [RUN_1209]

    experiments_data = []

    for run in RUNS:
        experiments_data.extend(analysis.analyse_run(run))

    statistical_results = analysis.analyse_statistics(experiments_data)

    analysis.apply_bh_correction(statistical_results)

    for experiment_name, result in statistical_results.items():
        print(f"\n{experiment_name}")

        for condition, comparisons in result["comparisons"].items():
            for control_type, comparison in comparisons.items():
                print(
                    f"{condition} vs {control_type}: "
                    f"{comparison['test']}, "
                    f"p = {comparison['p_value']:.4g}"
                    f"BH-adjusted p = {comparison['adjusted_p_value']:.4g}, "
                    f"significant = {comparison['significant']}"
                )

    plot.box_plot_experiments(
        experiments_data,
        statistical_results=statistical_results,
        save_individual=True,
        output_dir=run.output_dir,
    )


if __name__ == "__main__":
    main()
