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
    statistical_results: dict | None = None,
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
        sharey=False,
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

            if statistical_results is not None:
                result = statistical_results.get(experiment.name)

                if result is not None:
                    annotate_statistics(
                        ax=ax,
                        experiment=experiment,
                        data=data,
                        comparisons=result["comparisons"],
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

    plot_labels = (
        condition_order if condition_order is not None else list(plot_data.keys())
    )

    values = [plot_data[label] for label in plot_labels]

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


def add_pvalue_bracket(
    ax: plt.Axes,
    x1: int,
    x2: int,
    y: float,
    p_value: float,
    height: float,
) -> None:

    ax.plot(
        [x1, x1, x2, x2],
        [y, y + height, y + height, y],
        color="black",
        linewidth=1,
        clip_on=False,
    )

    ax.text(
        (x1 + x2) / 2,
        y + height,
        f"q = {p_value:.3g}",
        ha="center",
        va="bottom",
        fontsize=9,
    )


def annotate_statistics(
    ax: plt.Axes,
    experiment: entities.ExperimentConfig,
    data: dict[str, list[float]],
    comparisons: dict,
) -> None:

    order = experiment.condition_order

    all_values = np.concatenate(
        [np.asarray(values, dtype=float) for values in data.values()]
    )

    all_values = all_values[np.isfinite(all_values)]

    if len(all_values) == 0:
        return

    data_min = float(np.min(all_values))
    data_max = float(np.max(all_values))

    span = max(data_max - data_min, 0.1)

    height = 0.04 * span
    spacing = 0.14 * span

    bracket_index = 0

    for condition in experiment.experimental_conditions:
        if condition not in comparisons:
            continue

        for control_type, control_name in (
            ("negative_control", experiment.negative_control),
            ("specificity_control", experiment.specificity_control),
        ):
            if control_name is None:
                continue

            comparison = comparisons[condition].get(control_type)

            if comparison is None:
                continue

            p_value = comparison.get(
                "adjusted_p_value",
                comparison["p_value"],
            )

            x1 = order.index(condition) + 1
            x2 = order.index(control_name) + 1

            y = data_max + spacing * (bracket_index + 1)

            add_pvalue_bracket(
                ax=ax,
                x1=x1,
                x2=x2,
                y=y,
                p_value=p_value,
                height=height,
            )

            bracket_index += 1

    if bracket_index:
        ax.set_ylim(top=data_max + spacing * (bracket_index + 2))
