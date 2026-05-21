"""Configuration helpers for the synthetic FFR showcase."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class SimulationConfig:
    """Parameters for a deterministic MATLAB-style 5G FFR demo run."""

    seed: int = 202406
    snr_db: tuple[float, ...] = tuple(range(-5, 31, 5))
    user_density: tuple[int, ...] = (20, 40, 60, 80, 100, 120)
    methods: tuple[str, ...] = ("IFR3", "SWF", "FFR+IFR3", "FFR+SWF")
    cells: int = 19
    edge_fraction: float = 0.35
    monte_carlo_runs: int = 64
    bandwidth_mhz: float = 20.0
    noise_floor_dbm: float = -96.0
    reuse_penalty: dict[str, float] = field(
        default_factory=lambda: {
            "IFR3": 0.33,
            "SWF": 0.82,
            "FFR+IFR3": 0.58,
            "FFR+SWF": 0.74,
        }
    )
    interference_scale: dict[str, float] = field(
        default_factory=lambda: {
            "IFR3": 0.50,
            "SWF": 0.88,
            "FFR+IFR3": 0.34,
            "FFR+SWF": 0.28,
        }
    )


DEFAULT_CONFIG = SimulationConfig()
