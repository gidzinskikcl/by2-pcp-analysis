import matplotlib.pyplot as plt
from matplotlib.colors import to_rgba
import numpy as np

import pathlib

from plate_analysis import entities

medianprops = {
    "color": "#333333",
    "linewidth": 2,
}


def box_plot_experiments(
    experiments_data: list[tuple[entities.ExperimentConfig, dict[str, list[float]]]],
    save_individual: bool = False,
    output_dir: pathlib.Path = pathlib.Path("plots"),
) -> None:

    output_dir = pathlib.Path(output_dir)

    if save_individual:
        output_dir.mkdir(parents=True, exist_ok=True)

    n_experiments = len(experiments_data)

    fig, axes = plt.subplots(
        1,
        n_experiments,
        figsize=(5 * n_experiments, 8),
        squeeze=False,
        sharey=True,
    )

    axes = axes.flatten()

    for ax, (experiment, data) in zip(axes, experiments_data):
        box_plot_conditions(
            ax=ax,
            data=data,
            # labels=experiment.labels,
            condition_order=experiment.condition_order,
            controls=experiment.controls,
        )

        ax.set_title(experiment.name)

        if save_individual:
            individual_fig, individual_ax = plt.subplots(figsize=(6, 8))

            box_plot_conditions(
                ax=individual_ax,
                data=data,
                condition_order=experiment.condition_order,
                controls=experiment.controls,
            )
            individual_ax.set_title(experiment.name)
            individual_fig.tight_layout()
            filename = "".join(
                c if c.isalnum() or c in "-_" else "_" for c in experiment.name
            )

            individual_fig.savefig(
                output_dir / f"{filename}.png",
                dpi=300,
                bbox_inches="tight",
            )

            plt.close(individual_fig)

    plt.tight_layout()
    plt.show()


def box_plot_conditions(
    ax: plt.Axes,
    data: dict[str, list[float]],
    labels: dict[str, str] | None = None,
    condition_order: list[str] | None = None,
    controls: list[str] | None = None,
) -> None:
    """
    Creates a box plot for the given data.

    Args:
        data (dict): A dictionary where keys are condition names and values are lists of measurements.
    """
    if labels is None:
        labels = {condition: condition for condition in data}

    plot_data = {labels[condition]: values for condition, values in data.items()}

    plot_labels = list(plot_data.keys())
    values = list(plot_data.values())

    ax.set_axisbelow(True)
    ax.grid(
        linestyle="--",
        alpha=0.4,
    )

    # Make x and y axes thicker
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    ax.spines["bottom"].set_linewidth(1.5)
    ax.spines["left"].set_linewidth(1.5)

    # ax.tick_params(
    #     axis="both",
    #     width=1.5,
    #     length=5,
    # )

    ax.tick_params(axis="x", labelrotation=45)

    for label in ax.get_xticklabels():
        label.set_ha("right")

    boxplot = ax.boxplot(
        values,
        tick_labels=plot_labels,
        patch_artist=True,
        showfliers=False,
        medianprops=medianprops,
    )

    ax.set_ylabel("Normalised Chemiluminescence", fontsize=12)
    ax.set_xlabel("Condition", fontsize=12)

    colours = _generate_colours(controls=controls, labels=plot_labels)
    rng = np.random.default_rng(42)

    for i, (label, measurements, box) in enumerate(
        zip(plot_labels, values, boxplot["boxes"]),
        start=1,
    ):
        colour = colours[label]

        # Colour box
        box.set_facecolor(colour)
        box.set_facecolor(to_rgba(colour, alpha=0.4))
        box.set_edgecolor("black")

        # Individual measurements
        jitter = rng.normal(0, 0.06, size=len(measurements))

        ax.scatter(
            i + jitter,
            measurements,
            color=colour,
            alpha=0.8,
            zorder=3,
        )


def _generate_colours(labels: list[str], controls: list[str] = []) -> dict[str, str]:
    # Generate related colours for experimental conditions
    experimental_colours = plt.cm.Set2.colors

    colours = {}
    colour_index = 0

    for label in labels:
        if label in controls:
            colours[label] = "grey"
        else:
            colours[label] = experimental_colours[colour_index]
            colour_index += 1

    return colours
