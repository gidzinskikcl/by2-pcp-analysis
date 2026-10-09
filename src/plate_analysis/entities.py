from dataclasses import dataclass
from typing import Literal
import pathlib

NormalisationMethod = Literal["controls", "minmax"]


@dataclass
class ExperimentConfig:
    name: str

    experimental_conditions: list[str]

    positive_control: str
    source: dict[str, list[str]]
    labels: dict[str, str]

    negative_control: str | None = None
    specificity_control: str | None = None
    normalisation: NormalisationMethod = "controls"

    @property
    def controls(self) -> list[str]:
        return [
            control
            for control in [
                self.positive_control,
                self.negative_control,
                self.specificity_control,
            ]
            if control is not None
        ]

    @property
    def condition_order(self) -> list[str]:
        return [
            self.positive_control,
            *self.experimental_conditions,
            *([self.negative_control] if self.negative_control is not None else []),
            *(
                [self.specificity_control]
                if self.specificity_control is not None
                else []
            ),
        ]


@dataclass
class PlateInput:
    plate_id: str
    intensities_path: pathlib.Path


@dataclass
class RunConfig:
    plate_map_path: pathlib.Path
    plates: list[PlateInput]
    experiments: list[ExperimentConfig]
    output_dir: pathlib.Path
