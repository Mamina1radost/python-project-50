from typing import Union
from gendiff.schemas import JsonObject, YamlObject


def generate_tree(
    first: Union[JsonObject, YamlObject], second: Union[JsonObject, YamlObject]
) -> dict[str, Union[dict, str, int, bool]]:
    keys_all = get_keys(first, second)
    keys_all = set(keys_all)
    keys_all = list(keys_all)
    keys_all.sort()
    result_dict = {}
    for key in keys_all:
        find_diff(key, first, second, result_dict)
    return result_dict


def get_keys(first, second):
    if type(first) is dict and type(second) is dict:
        keys_all = list(first.keys()) + list(second.keys())
    elif type(first) is dict and type(second) is not dict:
        keys_all = list(first.keys())
    elif type(first) is not dict and type(second) is dict:
        keys_all = list(second.keys())
    else:
        keys_all = []
    return keys_all


def find_diff(key, first, second, result_dict):
    if key in first and key not in second:
        result_dict[key] = ["deleted", first[key]]
    elif key not in first and key in second:
        result_dict[key] = ["added", second[key]]
    elif isinstance(first.get(key), dict) and isinstance(second.get(key), dict):
        result_dict[key] = [
            "recursiv",
            generate_tree(first.get(key), second.get(key)),
        ]
    elif key in first and key in second:
        check_change(first, second, key, result_dict)


def check_change(first, second, key, result_dict):
    if first[key] == second[key]:
        result_dict[key] = ["unchanged", first[key]]
    elif first[key] != second[key]:
        result_dict[key] = ["changed", first[key], second[key]]
