import os

import pytest

PLUGINS_ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "plugins")


@pytest.fixture
def plugins_root():
    return PLUGINS_ROOT
