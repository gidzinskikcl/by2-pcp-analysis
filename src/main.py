from experiments.inf_1209 import RUN_1209
from plate_analysis import analysis, plot


def main():

    RUNS = [RUN_1209]

    experiments_data = []

    for run in RUNS:
        experiments_data.extend(analysis.analyse_run(run))

    plot.box_plot_experiments(
        experiments_data, save_individual=True, output_dir=run.output_dir
    )


if __name__ == "__main__":
    main()
