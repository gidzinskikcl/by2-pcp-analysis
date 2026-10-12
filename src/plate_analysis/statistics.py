import numpy as np

from scipy import stats
from statsmodels.stats.multitest import multipletests
from itertools import combinations


def descriptive_stats(
    grouped_data: dict[str, list[float]],
    plate_assignments: dict[str, list[str]] | None = None,
) -> dict[str, dict]:
    """
    plate_assignments: optional dict mapping condition -> list of plate IDs
    e.g. {"Construct A": ["plate1", "plate1", "plate2", ...]}
    """
    stats = {}

    for condition, values in grouped_data.items():
        arr = np.array(values)
        entry = {
            "n_wells": len(arr),
            "median": np.median(arr),
            "q1": np.percentile(arr, 25),
            "q3": np.percentile(arr, 75),
            "iqr": np.percentile(arr, 75) - np.percentile(arr, 25),
            "min": arr.min(),
            "max": arr.max(),
            "mean": arr.mean(),
            "sd": arr.std(ddof=1),
        }

        if plate_assignments:
            plates = plate_assignments[condition]
            entry["n_plates"] = len(set(plates))

        stats[condition] = entry

    return stats

    # Shapiro-Wilk normality tests


# A constant sample cannot meaningfully be assessed for normality.
def shapiro_p(values) -> float:
    if len(values) < 3 or np.ptp(values) == 0:
        return np.nan
    return float(stats.shapiro(values).pvalue)


def adjust_p_values(
    p_values: list[float],
    alpha: float = 0.05,
) -> tuple[list[float], list[bool]]:

    if not p_values:
        return [], []

    significant, adjusted, _, _ = multipletests(
        p_values,
        alpha=alpha,
        method="fdr_bh",
    )

    return adjusted.tolist(), significant.tolist()


def compare_conditions(
    experimental: list[float],
    control: list[float],
    test: str = "welch",
    alpha_normality: float = 0.05,
    min_wells_welsch: int = 9,
) -> dict[str, float]:
    """
    Compares two conditions using the Mann-Whitney U test.

    Args:
        experimental (list): A list of measurements for the experimental condition.
        control (list): A list of measurements for the control condition.

    Returns:
        dict: A dictionary containing the U statistic and p-value.
    """

    x = np.asarray(experimental, dtype=float)
    y = np.asarray(control, dtype=float)

    x = x[np.isfinite(x)]
    y = y[np.isfinite(y)]

    if len(x) < 3 or len(y) < 3:
        raise ValueError("At least 3 valid wells are required per condition.")

    # Descriptive effecti sizes
    median_difference = float(np.median(x) - np.median(y))
    mean_difference = float(np.mean(x) - np.mean(y))

    p_normality_x = shapiro_p(x)
    p_normality_y = shapiro_p(y)

    normal = (
        len(x) >= min_wells_welsch
        and len(y) >= min_wells_welsch
        and np.isfinite(p_normality_x)
        and np.isfinite(p_normality_y)
        and p_normality_x > alpha_normality
        and p_normality_y > alpha_normality
    )

    # if normal:
    #     test = "welch"
    #     score = stats.ttest_ind(
    #         x,
    #         y,
    #         equal_var=False,
    #         alternative="less",
    #     )
    # else:
    #     test = "mann_whitneyu"
    #     score = stats.mannwhitneyu(
    #         x,
    #         y,
    #         alternative="less",
    #     )

    if test == "welch":
        score = stats.ttest_ind(
            x,
            y,
            equal_var=False,
            alternative="less",
        )

    elif test == "mann_whitneyu":
        score = stats.mannwhitneyu(
            x,
            y,
            alternative="less",
        )

    else:
        raise ValueError(f"Unknown statistical test: {test}")

    result = {
        "n_experimental": len(x),
        "n_control": len(y),
        "mean_difference": mean_difference,
        "median_difference": median_difference,
        "p_normality_experimental": p_normality_x,
        "p_normality_control": p_normality_y,
        "test": test,
        "statistic": float(score.statistic),
        "p_value": float(score.pvalue),
    }

    return result


def compare_candidates(
    data: dict[str, list[float]],
    candidates: list[str],
) -> dict[str, dict]:

    comparisons = {}

    for candidate_a, candidate_b in combinations(candidates, 2):

        x = np.asarray(data[candidate_a], dtype=float)
        y = np.asarray(data[candidate_b], dtype=float)

        x = x[np.isfinite(x)]
        y = y[np.isfinite(y)]

        if len(x) < 3 or len(y) < 3:
            raise ValueError("At least 3 valid wells required per candidate")

        score = stats.ttest_ind(
            x,
            y,
            equal_var=False,
            alternative="two-sided",
        )

        comparisons[(candidate_a, candidate_b)] = {
            "test": "welch",
            "statistic": float(score.statistic),
            "p_value": float(score.pvalue),
            "mean_difference": float(np.mean(x) - np.mean(y)),
            "median_difference": float(np.median(x) - np.median(y)),
        }

    return comparisons
