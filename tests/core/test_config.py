import pytest
import yaml
import os

from core.config import Config
from core.config_reader import read


@pytest.fixture
def sites_file():
    config_path = os.path.dirname(os.path.realpath(os.path.curdir))
    sites_file = os.path.join(config_path, "{}{}{}".format('config', os.path.sep, 'config.yaml'))
    return sites_file


def test_config_reader(sites_file):
    config = Config(sites_file)

    print(config)
    assert config is not None
    assert config.urls is not None
    assert config.tags is not None
    assert type(config.urls) is list
    assert type(config.tags) is list