from typing import Any, Callable, Dict, List, Optional, Tuple


def serialize_string(value: Optional[str]) -> str:
    return str(value) if value else ""


def deserialize_string(value: str) -> str:
    return str(value)


def serialize_bool(value: Optional[str]) -> bool:
    return value == "True"


def deserialize_bool(value: bool) -> str:
    return "True" if value else "False"


def serialize_int(value: Optional[str]) -> int:
    return int(value or 0)


def deserialize_int(value: str) -> str:
    return str(value or 0)


def serialize_list(value: Optional[str]) -> List[str]:
    if value:
        return [x for x in value.split(",") if x]
    return []


def deserialize_list(value: List[str]) -> str:
    return ",".join(value) if value else ""


def noop(value: Optional[str]) -> str:
    return value or ""


Serializer = Callable[[Any], Any]
Deserializer = Callable[[Any], Any]


TYPES_SERIALIZERS: Dict[str, Tuple[Serializer, Deserializer]] = {
    "string": (serialize_string, deserialize_string),
    "bool": (serialize_bool, deserialize_bool),
    "int": (serialize_int, deserialize_int),
    "list": (serialize_list, deserialize_list),
    "image": (noop, noop),
}


def serialize_value(python_type: str, value: Optional[str]):
    try:
        serializer = TYPES_SERIALIZERS[python_type][0]
    except KeyError:
        raise ValueError(f"'{python_type}' type is not serializeable.")

    return serializer(value)


def deserialize_value(python_type: str, value: Any):
    try:
        deserializer = TYPES_SERIALIZERS[python_type][1]
    except KeyError:
        raise ValueError(f"'{python_type}' type is not deserializeable.")

    return deserializer(value)
