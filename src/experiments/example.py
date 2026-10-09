import pathlib
from plate_analysis import entities

DATA_DIR = pathlib.Path("/file/path/to/your/infiltration/results")

EXPERIMENTS = [
    entities.ExperimentConfig(
        name="Candidate X × Effector A",
        experimental_conditions=["A"],
        positive_control="Rx + PVX-CP",
        negative_control="PTO",
        specificity_control="PVX-CP",
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

RUN_1209 = entities.RunConfig(
    plate_map_path=DATA_DIR / "PCPs.xlsx",
    plates=[
        entities.PlateInput(
            plate_id="(plate_number)",
            intensities_path=DATA_DIR
            / ("Path/to/csv/with/chemiluminescence/intensities"),
        ),
    ],
    experiments=EXPERIMENTS,
    output_dir=DATA_DIR / "analysis",
)
