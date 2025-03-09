import pytest

from analysis import Analyzer


@pytest.fixture
def analyzer():
    """Fixture to create an Analyzer instance for testing."""
    return Analyzer()


def test_add_measurements_valid(analyzer):
    """Test adding valid physiological data."""
    data = {"Respiration": 14, "Rate": 80, "Level": 3, "Dilation": 5}
    analyzer.add_measurements(data)

    assert analyzer.respiration == [14]
    assert analyzer.heart_rate == [80]
    assert analyzer.blushing_level == [3]
    assert analyzer.pupillary_dilation == [5]


def test_add_measurements_invalid(analyzer):
    """Test adding invalid data (non-integer values)."""
    data = {"Respiration": "fast", "Rate": "high", "Level": "none", "Dilation": "wide"}

    with pytest.raises(ValueError):
        analyzer.add_measurements(data)


def test_check_respiration(analyzer):
    """Test respiration check logic."""
    analyzer.respiration = [12, 14, 16]
    assert analyzer.check_respiration() is True


def test_check_respiration_invalid_too_low(analyzer):
    """Test respiration check logic."""
    analyzer.respiration = [0, 0, 0]
    assert analyzer.check_respiration() is False


def test_check_respiration_invalid_too_high(analyzer):
    """Test respiration check logic."""
    analyzer.respiration = [100, 100, 100]
    assert analyzer.check_respiration() is False


def test_check_heart_rate(analyzer):
    """Test heart rate check logic."""
    analyzer.heart_rate = [60, 80, 100]
    assert analyzer.check_heart_rate() is True


def test_check_heart_rate_invalid_too_low(analyzer):
    """Test heart rate check logic."""
    analyzer.heart_rate = [0, 0, 0]
    assert analyzer.check_heart_rate() is False


def test_check_heart_rate_invalid_too_high(analyzer):
    """Test heart rate check logic."""
    analyzer.heart_rate = [600, 800, 1000]
    assert analyzer.check_heart_rate() is False


def test_decision_human(analyzer):
    """Test decision function when values indicate a human."""
    analyzer.respiration = [14, 15]
    analyzer.heart_rate = [70, 75]
    analyzer.blushing_level = [3, 4]
    analyzer.pupillary_dilation = [4, 5]

    assert analyzer.decision() == "палюбому человек aga"


def test_decision_replicant(analyzer):
    """Test decision function when values indicate a replicant."""
    analyzer.respiration = [10]
    analyzer.heart_rate = [110]
    analyzer.blushing_level = [6]
    analyzer.pupillary_dilation = [9]

    assert analyzer.decision() == "уже не человек sadding"


if __name__ == '__main__':
    pytest.main()
