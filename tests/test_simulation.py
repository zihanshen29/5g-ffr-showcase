from ffr_showcase.simulation import run_alignment


def test_alignment_has_expected_methods_and_metrics():
    data = run_alignment()
    assert set(data["method"]) == {"IFR3", "SWF", "FFR+IFR3", "FFR+SWF"}
    assert {"capacity_mbps", "edge_sinr_db", "interference_index"}.issubset(data.columns)
    assert len(data) > 0


def test_capacity_values_are_positive():
    data = run_alignment()
    assert (data["capacity_mbps"] > 0).all()
    assert (data["spectral_efficiency_bps_hz"] > 0).all()
