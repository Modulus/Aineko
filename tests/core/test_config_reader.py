import pytest
from core.config_reader import read


@pytest.fixture
def sites_file():
    sites_file = "config/sites.yaml"
    return sites_file


def test_config_reader(sites_file):
    data = read("config/sites.yaml")
    assert data is not None
    assert "sites" in data
    assert "http://vg.no" in data["sites"]
    assert "http://www.dagbladet.no" in data["sites"]
    assert "http://www.dn.no" in data["sites"]
    assert "http://e24.no" in data["sites"]
