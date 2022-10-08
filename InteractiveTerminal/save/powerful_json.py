import json
import inspect
from dataclasses import field, is_dataclass, fields
from enum import Enum, IntEnum
import importlib


def to_dict(obj):
    assert not isinstance(obj, type), f"Serializing type, not instance: {obj}"
    if is_dataclass(obj) or isinstance(obj, Enum) or isinstance(obj, IntEnum):
        modname = inspect.getmodule(obj).__name__
        classname = type(obj).__name__
        full_type = f"{modname}|{classname}"

        if is_dataclass(obj):
            d = {
                "__type__": full_type,
            }

            for each_field in fields(obj):
                if each_field.init and not each_field.metadata.get(
                    "IGNORESAVE", False
                ):
                    d[each_field.name] = to_dict(getattr(obj, each_field.name))

            return d

        elif isinstance(obj, Enum):
            d = {"__type__": full_type, "value": obj.value}

            return d

    return obj


class PowerfulEncoder(json.JSONEncoder):
    def default(self, o):
        return to_dict(o)


def from_dict(obj):
    if isinstance(obj, dict) and "__type__" in obj:
        full_type = obj.pop("__type__")
        modname, classname = full_type.split("|")
        clazz = getattr(importlib.import_module(modname), classname)
        return clazz(**obj)
    else:
        return obj


def loads(s, **kwargs):
    return json.loads(s, object_hook=from_dict, **kwargs)


def dumps(obj, **kwargs):
    return json.dumps(obj, cls=PowerfulEncoder, **kwargs)
