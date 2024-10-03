from typing import Union
from gendiff.schemas import JsonObject, YamlObject


def rekursive_diff(
    first: Union[JsonObject, YamlObject], second: Union[JsonObject, YamlObject]
) -> dict[str, Union[dict, str, int, bool]]:
    if type(first) is dict and type(second) is dict:
        keys_all = list(first.keys()) + list(second.keys())
    elif type(first) is dict and type(second) is not dict:
        keys_all = list(first.keys())
    else:
        keys_all = list(second.keys())
    keys_all = set(keys_all)
    keys_all = list(keys_all)
    keys_all.sort()
    result_dict = {}
    for key in keys_all:
        if key in first and key not in second:
            result_dict[key] = ["deleted", first[key]]
        elif key not in first and key in second:
            result_dict[key] = ["added", second[key]]
        elif isinstance(first.get(key), dict) and isinstance(second.get(key), dict):
            result_dict[key] = [
                "recursiv",
                rekursive_diff(first.get(key), second.get(key)),
            ]
        elif key in first and key in second:
            if first[key] == second[key]:
                result_dict[key] = ["unchanged", first[key]]
            elif first[key] != second[key]:
                result_dict[key] = ["changed", first[key], second[key]]
    return result_dict
