from unittest.mock import Mock

from aiodataloader import DataLoader

from ..loader import get_loader, positive_int


def test_loader_factory_returns_loader_instance():
    loader = get_loader({}, "test_loader", Mock())
    assert isinstance(loader, DataLoader)


def test_loader_factory_creates_named_loader_instance_on_current_context():
    context = {}
    loader = get_loader(context, "test_loader", Mock())
    assert context
    assert loader in context.values()


def test_loader_factory_returns_already_existing_loader_instance_from_current_context():
    context = {}
    loader = get_loader(context, "test_loader", Mock())
    assert get_loader(context, "test_loader", Mock()) is loader


def test_positive_int_parses_valid_int_str_repr_to_int():
    assert positive_int("1") == 1


def test_positive_int_returns_none_if_string_couldnt_be_parsed():
    assert positive_int("abc") is None


def test_positive_int_returns_none_if_string_contained_zero():
    assert positive_int("0") is None


def test_positive_int_returns_none_if_string_contained_negative_int():
    assert positive_int("-1") is None
