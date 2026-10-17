from dataclasses import dataclass, field
from typing import Literal
import pathlib

NormalisationMethod = Literal["controls", "minmax"]


@dataclass
class ExperimentConfig:
    name: str

    experimental_conditions: list[str]

    source: dict[str, list[str]]
    labels: dict[str, str]

    positive_control: str | None = None
    negative_control: str | None = None
    specificity_controls: list[str] = field(default_factory=list)
    normalisation: NormalisationMethod = "controls"

    @property
    def controls(self) -> list[str]:
        return [
            *([self.positive_control] if self.positive_control is not None else []),
            *([self.negative_control] if self.negative_control is not None else []),
            *self.specificity_controls,
        ]

    @property
    def condition_order(self) -> list[str]:
        return [
            *([self.positive_control] if self.positive_control is not None else []),
            *self.experimental_conditions,
            *([self.negative_control] if self.negative_control is not None else []),
            *self.specificity_controls,
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
