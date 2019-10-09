import pytest

from ..base import Input


def test_processing_base_input_raises_not_implemented_error():
    input_type = Input()
    with pytest.raises(NotImplementedError):
        input_type.process(None)
