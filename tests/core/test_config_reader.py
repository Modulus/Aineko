import pytest
import yaml
import os
from core.config_reader import read


@pytest.fixture
def sites_file():
    config_path = os.path.dirname(os.path.realpath(__file__))
    sites_file = os.path.join(config_path, "{}{}{}".format('config', os.path.sep, 'sites.yaml'))
    return sites_file


def test_config_reader(sites_file):
    data = read("config/sites.yaml")
    assert data is not None
    assert "sites" in data
    assert "http://www.vg.no" in data["sites"]
    assert "http://dagbladet.no" in data["sites"]
    assert "http://www.dn.no" in data["sites"]
    assert "http://e24.no" in data["sites"]
