from ffr_showcase.trends import verify_trends


def test_synthetic_trends_pass():
    checks = verify_trends()
    assert checks["all_passed"], checks
