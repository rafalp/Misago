from typing import List

import pytest

from click.testing import CliRunner, Result

from .. import cli


@pytest.fixture
def invoke_cli():
    def invoke(*args: List[str]) -> Result:
        runner = CliRunner()
        return runner.invoke(cli, args)

    return invoke
