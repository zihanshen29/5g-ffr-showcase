"""Deterministic synthetic simulation for a 5G FFR paper-style showcase."""

from __future__ import annotations

from dataclasses import asdict
from pathlib import Path

import numpy as np
import pandas as pd

from .config import SimulationConfig


def _hex_ring_coordinates(radius: int = 2) -> np.ndarray:
    """Return axial hex-grid coordinates for the first 19 cells."""

    coords: list[tuple[int, int]] = []
    for q in range(-radius, radius + 1):
        for r in range(-radius, radius + 1):
            s = -q - r
            if max(abs(q), abs(r), abs(s)) <= radius:
                coords.append((q, r))
    coords.sort(key=lambda item: (max(abs(item[0]), abs(item[1]), abs(-item[0] - item[1])), item[0], item[1]))
    return np.array(coords, dtype=float)


def _interference_matrix(cells: int) -> np.ndarray:
    coords = _hex_ring_coordinates()[:cells]
    delta = coords[:, None, :] - coords[None, :, :]
    distance = np.sqrt(delta[..., 0] ** 2 + delta[..., 1] ** 2 + delta[..., 0] * delta[..., 1])
    matrix = np.where(distance > 0, 1.0 / np.maximum(distance, 1.0) ** 3.2, 0.0)
    return matrix / matrix.max()


def _method_factor(method: str, snr_db: float, density: int, config: SimulationConfig) -> tuple[float, float]:
    reuse = config.reuse_penalty[method]
    interference = config.interference_scale[method]
    water_filling_gain = 1.0 + (0.10 if "SWF" in method else 0.0) * np.tanh((snr_db - 5.0) / 12.0)
    density_pressure = 1.0 + 0.0035 * max(density - 40, 0)
    return reuse * water_filling_gain, interference * density_pressure


def simulate_point(
    snr_db: float,
    density: int,
    method: str,
    config: SimulationConfig,
    rng: np.random.Generator,
) -> dict[str, float | int | str]:
    coupling = _interference_matrix(config.cells)
    users = rng.poisson(lam=density, size=config.cells).clip(min=1)
    fading = rng.rayleigh(scale=1.0, size=(config.monte_carlo_runs, config.cells))
    shadowing_db = rng.normal(loc=0.0, scale=2.0, size=(config.monte_carlo_runs, config.cells))
    snr_linear = 10.0 ** (snr_db / 10.0)
    reuse_factor, interference_factor = _method_factor(method, snr_db, density, config)

    channel_gain = fading * 10.0 ** (shadowing_db / 10.0)
    inter_cell_load = coupling @ (users / users.mean())
    interference = interference_factor * inter_cell_load[None, :] * (0.25 + 0.02 * np.log1p(snr_linear))
    sinr = (snr_linear * channel_gain) / (1.0 + interference)

    edge_cells = np.argsort(inter_cell_load)[-max(1, int(config.cells * config.edge_fraction)) :]
    spectral_eff = np.log2(1.0 + sinr)
    capacity = config.bandwidth_mhz * reuse_factor * spectral_eff.mean(axis=1).sum()
    edge_capacity = config.bandwidth_mhz * reuse_factor * spectral_eff[:, edge_cells].mean(axis=1).sum()
    edge_sinr_db = 10.0 * np.log10(np.maximum(sinr[:, edge_cells].mean(), 1e-12))

    return {
        "snr_db": snr_db,
        "user_density": density,
        "method": method,
        "capacity_mbps": float(capacity / config.monte_carlo_runs),
        "spectral_efficiency_bps_hz": float(spectral_eff.mean() * reuse_factor),
        "edge_capacity_mbps": float(edge_capacity / config.monte_carlo_runs),
        "edge_sinr_db": float(edge_sinr_db),
        "interference_index": float(interference.mean()),
    }


def run_alignment(config: SimulationConfig | None = None) -> pd.DataFrame:
    config = config or SimulationConfig()
    rng = np.random.default_rng(config.seed)
    rows = []
    for density in config.user_density:
        for snr_db in config.snr_db:
            for method in config.methods:
                rows.append(simulate_point(snr_db, density, method, config, rng))
    return pd.DataFrame(rows)


def write_alignment_outputs(output_dir: str | Path, config: SimulationConfig | None = None) -> Path:
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    config = config or SimulationConfig()
    results = run_alignment(config)
    csv_path = output_path / "paper_alignment_synthetic.csv"
    results.to_csv(csv_path, index=False)
    metadata = pd.Series(asdict(config), name="value")
    metadata.to_json(output_path / "run_metadata.json", indent=2)
    return csv_path
