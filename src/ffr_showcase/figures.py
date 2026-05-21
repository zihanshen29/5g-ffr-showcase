"""Figure generation for the synthetic FFR showcase."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

from .simulation import run_alignment


def _load_or_run(results_csv: str | Path | None = None) -> pd.DataFrame:
    if results_csv and Path(results_csv).exists():
        return pd.read_csv(results_csv)
    return run_alignment()


def generate_figures(output_dir: str | Path, results_csv: str | Path | None = None) -> list[Path]:
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    data = _load_or_run(results_csv)
    density_values = sorted(data["user_density"].unique())
    density = density_values[len(density_values) // 2]
    snr_data = data[data["user_density"] == density]

    figure_paths: list[Path] = []
    fig, ax = plt.subplots(figsize=(8, 5))
    for method, group in snr_data.groupby("method"):
        group = group.sort_values("snr_db")
        ax.plot(group["snr_db"], group["capacity_mbps"], marker="o", label=method)
    ax.set_title("Fig.3 Synthetic Capacity vs SNR")
    ax.set_xlabel("SNR (dB)")
    ax.set_ylabel("Average network capacity (Mbps)")
    ax.grid(True, alpha=0.3)
    ax.legend()
    path = output_path / "fig3_capacity_vs_snr.png"
    fig.tight_layout()
    fig.savefig(path, dpi=160)
    plt.close(fig)
    figure_paths.append(path)

    fig, ax = plt.subplots(figsize=(8, 5))
    for method, group in snr_data.groupby("method"):
        group = group.sort_values("snr_db")
        ax.plot(group["snr_db"], group["edge_sinr_db"], marker="s", label=method)
    ax.set_title("Fig.4 Synthetic Edge SINR vs SNR")
    ax.set_xlabel("SNR (dB)")
    ax.set_ylabel("Mean edge-user SINR (dB)")
    ax.grid(True, alpha=0.3)
    ax.legend()
    path = output_path / "fig4_edge_sinr_vs_snr.png"
    fig.tight_layout()
    fig.savefig(path, dpi=160)
    plt.close(fig)
    figure_paths.append(path)

    density_data = data[data["snr_db"] == 15]
    fig, ax = plt.subplots(figsize=(8, 5))
    for method, group in density_data.groupby("method"):
        group = group.sort_values("user_density")
        ax.plot(group["user_density"], group["interference_index"], marker="^", label=method)
    ax.set_title("Synthetic Interference vs User Density")
    ax.set_xlabel("Mean users per cell")
    ax.set_ylabel("Interference index")
    ax.grid(True, alpha=0.3)
    ax.legend()
    path = output_path / "interference_vs_density.png"
    fig.tight_layout()
    fig.savefig(path, dpi=160)
    plt.close(fig)
    figure_paths.append(path)

    return figure_paths
