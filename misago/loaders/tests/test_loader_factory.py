from unittest.mock import Mock

from aiodataloader import DataLoader

from ..loader import get_loader


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
