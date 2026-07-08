"""Trend checks for synthetic paper-alignment outputs."""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from .simulation import run_alignment


def _load_or_run(results_csv: str | Path | None = None) -> pd.DataFrame:
    if results_csv is None:
        return run_alignment()
    return pd.read_csv(results_csv)


def verify_trends(results_csv: str | Path | None = None) -> dict[str, bool]:
    data = _load_or_run(results_csv)
    density_values = sorted(data["user_density"].unique())
    mid_density = density_values[len(density_values) // 2]
    snr_slice = data[data["user_density"] == mid_density]

    capacity_monotonic = all(
        group.sort_values("snr_db")["capacity_mbps"].is_monotonic_increasing
        for _, group in snr_slice.groupby("method")
    )

    edge = snr_slice[snr_slice["snr_db"] == snr_slice["snr_db"].max()].set_index("method")
    swf_linear = 10.0 ** (edge.loc["SWF", "edge_sinr_db"] / 10.0)
    ffr_swf_linear = 10.0 ** (edge.loc["FFR+SWF", "edge_sinr_db"] / 10.0)
    ffr_edge_profile = (
        edge.loc["FFR+IFR3", "edge_sinr_db"] > edge.loc["IFR3", "edge_sinr_db"]
        and ffr_swf_linear >= 0.75 * swf_linear
    )

    dense = data[data["snr_db"] == 15].groupby(["method", "user_density"])["interference_index"].mean()
    density_pressure = all(
        dense.loc[method].sort_index().iloc[-1] > dense.loc[method].sort_index().iloc[0]
        for method in data["method"].unique()
    )

    swf_capacity_advantage = (
        edge.loc["SWF", "capacity_mbps"] > edge.loc["IFR3", "capacity_mbps"]
        and edge.loc["FFR+SWF", "capacity_mbps"] > edge.loc["FFR+IFR3", "capacity_mbps"]
    )

    checks = {
        "capacity_increases_with_snr": bool(capacity_monotonic),
        "ffr_edge_profile_valid": bool(ffr_edge_profile),
        "interference_grows_with_density": bool(density_pressure),
        "swf_improves_capacity": bool(swf_capacity_advantage),
    }
    checks["all_passed"] = all(checks.values())
    return checks
