import pytest

from ..base import Input


def test_processing_base_input_raises_strict_error():
    input_type = Input()
    with pytest.raises(TypeError):
        input_type.process(None)
