from unittest.mock import Mock

import pytest

from ..exceptions import HTTPNotFound
from ..utils import clean_id_or_404


def test_clean_id_is_returned_from_request():
    request = Mock(path_params={"id": "123"})
    clean_id = clean_id_or_404(request)
    assert clean_id == 123


def test_clean_id_raises_not_found_exception_if_id_is_not_set():
    with pytest.raises(HTTPNotFound):
        request = Mock(path_params={})
        clean_id_or_404(request)


def test_clean_id_raises_not_found_exception_if_id_is_invalid():
    with pytest.raises(HTTPNotFound):
        request = Mock(path_params={"id": "invalid"})
        clean_id_or_404(request)


def test_clean_id_raises_not_found_exception_if_id_is_less_than_1():
    with pytest.raises(HTTPNotFound):
        request = Mock(path_params={"id": "0"})
        clean_id_or_404(request)

    with pytest.raises(HTTPNotFound):
        request = Mock(path_params={"id": -1})
        clean_id_or_404(request)
