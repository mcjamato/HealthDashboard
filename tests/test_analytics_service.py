import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from services.analytics_service import AnalyticsService


def test_percent_change():
    assert AnalyticsService.percent_change([100, 110]) == 10


def test_percent_change_zero_baseline():
    assert AnalyticsService.percent_change([0, 10]) is None
