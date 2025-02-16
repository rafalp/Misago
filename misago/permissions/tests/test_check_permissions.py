import pytest
from django.core.exceptions import PermissionDenied
from django.http import Http404

from ..checkutils import check_permissions


def test_check_permissions_is_true_if_checks_passed():
    with check_permissions() as check:
        pass

    assert check
    assert not check.error
    assert not check.not_found
    assert not check.permission_denied


def test_check_permissions_is_true_if_unsupported_exception_was_raised():
    with pytest.raises(ValueError):
        with check_permissions() as check:
            raise ValueError()

    assert check
    assert not check.error
    assert not check.not_found
    assert not check.permission_denied


def test_check_permissions_is_false_if_http404_exception_was_raised():
    with check_permissions() as check:
        raise Http404()

    assert not check
    assert check.error
    assert check.not_found
    assert not check.permission_denied


def test_check_permissions_is_false_if_permission_exception_was_raised():
    with check_permissions() as check:
        raise PermissionDenied()

    assert not check
    assert check.error
    assert not check.not_found
    assert check.permission_denied
