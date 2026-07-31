from ..extensions import ExtensionRegistry


class Base:
    def lorem(self):
        return "lorem"

    def ipsum(self):
        return "ipsum"


class Dolor:
    def lorem(self):
        return super().lorem() + "dolor"


class Met:
    def lorem(self):
        return super().lorem() + "met"

    def ipsum(self):
        return super().ipsum() + "met"


def test_extension_registry_returns_base_type_if_no_extensions():
    extensions = ExtensionRegistry()
    assert extensions.get(Base) is Base


def test_extension_registry_extends_base_type_with_single_extension():
    extensions = ExtensionRegistry()
    extensions.register(Base, Dolor)

    ExtendedBase = extensions.get(Base)
    assert ExtendedBase is not Base
    assert ExtendedBase().lorem() == "loremdolor"


def test_extension_registry_extends_base_type_with_multiple_extensions():
    extensions = ExtensionRegistry()
    extensions.register(Base, Dolor)
    extensions.register(Base, Met)

    ExtendedBase = extensions.get(Base)
    assert ExtendedBase is not Base
    assert ExtendedBase().lorem() == "loremdolormet"


def test_extension_registry_prepends_extension():
    extensions = ExtensionRegistry()
    extensions.register(Base, Dolor)
    extensions.register(Base, Met, prepend=True)

    ExtendedBase = extensions.get(Base)
    assert ExtendedBase is not Base
    assert ExtendedBase().lorem() == "loremmetdolor"


def test_extension_registry_caches_extended_type():
    extensions = ExtensionRegistry()
    extensions.register(Base, Dolor)

    ExtendedBase1 = extensions.get(Base)
    ExtendedBase2 = extensions.get(Base)
    assert ExtendedBase1 is not Base
    assert ExtendedBase2 is not Base
    assert ExtendedBase1 is ExtendedBase2


def test_extension_registry_invalidates_cache_for_extended_type():
    extensions = ExtensionRegistry()

    extensions.register(Base, Dolor)
    ExtendedBase1 = extensions.get(Base)
    assert ExtendedBase1 is not Base
    assert ExtendedBase1().lorem() == "loremdolor"

    extensions.register(Base, Met)
    ExtendedBase2 = extensions.get(Base)
    assert ExtendedBase2 is not Base
    assert ExtendedBase2 is not ExtendedBase1
    assert ExtendedBase2().lorem() == "loremdolormet"
