import os

import pytest
from rx import Observable

from core.config import Config
from core.internal.papers_observer import PapersObserver


# @pytest.fixture
# def sites_file():
#     current_path = os.path.dirname(os.path.abspath(__file__))
#     config_path =  os.path.abspath(os.path.join(current_path, os.pardir, os.pardir))
#     sites_file = os.path.join(config_path, "{}{}{}".format('config', os.path.sep, 'sites.yaml'))
#     return sites_file
#
#
# def test_stuff():
#
#     config = Config(sites_file())
#
#     source = Observable.from_(config.urls)
#
#     source.subscribe(PapersObserver("localhost:9200"))