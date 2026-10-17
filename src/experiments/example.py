import pathlib
from src.plate_analysis import config

DATA_DIR = pathlib.Path("/file/path/to/your/infiltration/results")

EXPERIMENTS = [
    config.ExperimentConfig(
        name="Candidate X × Effector A",
        experimental_conditions=["A"],
        positive_control="Rx + PVX-CP",
        negative_control="PTO",
        specificity_controls=["PVX-CP"],
        normalisation="controls",
        source={
            "(plate_number)": [
                "Rx + CP",
                "CAN_X",
                "CAN_X+PTO",
                "CAN_X+CP",
            ],
        },
        labels={
            "Rx + CP": "Rx + PVX-CP",
            "CAN_X": "A",
            "CAN_X+PTO": "PTO",
            "CAN_X+CP": "PVX-CP",
        },
    )
]

RUN_1209 = config.RunConfig(
    plate_map_path=DATA_DIR / "PCPs.xlsx",
    plates=[
        config.PlateInput(
            plate_id="(plate_number)",
            intensities_path=DATA_DIR
            / ("Path/to/csv/with/chemiluminescence/intensities"),
        ),
    ],
    experiments=EXPERIMENTS,
    output_dir=DATA_DIR / "analysis",
)
