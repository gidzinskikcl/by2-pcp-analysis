# BY-2 PCP Analysis

Python tools for plate mapping, chemiluminescence quantification, and analysis of BY-2 Plant Cell Pack (PCP) transient expression assays.

## Setup
```
# Go to repo root
cd path/to/folder/by2-pcp-analysis

# Create the virtual environment
python3 -m venv .by2-pcp-venv

# Activate it
source .by2-pcp-venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# When you're finished
deactivate
```
In order to activate the environment again, use the same command as before

## Running an Analysis

Each infiltration run is configured using a Python file in the experiments/ directory. This allows you to analyse different experiments without modifying the analysis pipeline.

### 1. Create an experiment configuration

Create a new Python file in experiments/, for example inf_1209.py. You can copy an existing configuration and modify it for your new experiment.

Each configuration defines:

**Plate map:** Path to the Excel file containing the 96-well plate layouts.

**Plates:** Plate IDs and their corresponding Fiji chemiluminescence intensity CSV files.

**Experiments:** Conditions to analyse, their controls, labels, and normalisation settings.

A single run can contain multiple plates and experiments. An experiment can combine measurements from several plates, and different experiments can use different conditions from the same plate.

## 2. Configure the plates

Specify the plate map and the intensity CSV file for each plate.

```
from pathlib import Path
from plate_analysis import entities

DATA_DIR = Path("/path/to/labbook/INF_1209")

PLATE_MAP_PATH = DATA_DIR / "PCPs_1209.xlsx"

PLATES = [
    entities.PlateInput(
        plate_id="3",
        intensities_path=DATA_DIR / "plate3_intensities.csv",
    ),
    entities.PlateInput(
        plate_id="4",
        intensities_path=DATA_DIR / "plate4_intensities.csv",
    ),
]
```
Plate IDs must match those defined in the Excel plate map.

### 3. Configure the experiments

Define each experiment using ExperimentConfig.

```
EXPERIMENTS = [
    entities.ExperimentConfig(
        name="Rx113 × SRE33",
        experimental_conditions=["SRE33"],
        positive_control="Rx + PVX-CP",
        negative_control="PTO",
        specificity_control="PVX-CP",
        source={
            "3": [
                "Rx + CP",
                "CAN113",
                "CAN113+PTO",
                "CAN113+CP",
            ],
            "4": [
                "CAN113",
                "CAN113+PTO",
            ],
        },
        labels={
            "Rx + CP": "Rx + PVX-CP",
            "CAN113": "SRE33",
            "CAN113+PTO": "PTO",
            "CAN113+CP": "PVX-CP",
        },
    ),
]
```
The source dictionary determines which measurements belong to an experiment. Conditions from multiple plates are combined into the same experiment.

The labels dictionary translates condition names from the Excel plate map into readable labels used in the plots.

### 5. Create the run configuration

At the bottom of the configuration file, combine the plate map, plates, and experiments into a RunConfig.

```
RUN_1209 = entities.RunConfig(
    plate_map_path=PLATE_MAP_PATH,
    plates=PLATES,
    experiments=EXPERIMENTS,
)
```

### 6. Run the analysis

In src/main.py, import the run configuration:
```
from experiments.inf_1209 import RUN_1209
from plate_analysis import analysis, plot

def main():
    experiments_data = analysis.analyse_run(RUN_1209)
...
..
.
```
The script will:

Read the Excel plate maps and corresponding Fiji intensity CSV files.

Match intensity measurements to wells and conditions.

Select the measurements belonging to each configured experiment.

Group and normalise the measurements independently for each experiment.

Generate a combined figure containing all experiments as separate subplots.

