import argparse
import json
import yaml
from pathlib import Path
from gendiff.schemas import JsonObject, YamlObject
from typing import Union
from yaml.loader import SafeLoader
from gendiff.formatters.stylish import BASE_TAB, formater
from gendiff.formatters.plain import plain


def main():
    parser = argparse.ArgumentParser(
        description="Compares two configuration files and shows a difference."
    )

    parser.add_argument("first_file")
    parser.add_argument("second_file")
    parser.add_argument("-f", "--format", help="set format of output")


    args = parser.parse_args()
    first_file, second_file = load_json_or_yaml(args.first_file, args.second_file)

    first, second = generate_diff(first_file, second_file)
    if args.format == 'plain':
        return plain(rekursive_diff(first, second)).rstrip('\n')
    if args.format == 'stylish':
        return formater(0, rekursive_diff(first, second)).rstrip('\n')


def load_json_or_yaml(first, second):
    suf_first = Path(first).suffix
    suf_second = Path(second).suffix
    if suf_first == '.json':
        first_file = json.load(open(first))
    if suf_second == '.json':
        second_file = json.load(open(second))
    if suf_first == '.yaml' or suf_first =='.yml':
        first_file = yaml.load(open(first), Loader=SafeLoader)
    if suf_second == '.yaml' or suf_second =='.yml':
        second_file = yaml.load(open(second), Loader=SafeLoader)
    return first_file, second_file


def generate_diff(first: Union[JsonObject, YamlObject], second: Union[JsonObject, YamlObject]) -> str:
    keys_all = list(first.keys()) + list(second.keys())
    keys_all = set(keys_all)
    keys_all = list(keys_all)
    keys_all.sort()
    with open('res.txt', 'w') as f:
        print(plain(rekursive_diff(first, second)), file=f)
    #return formater(0, rekursive_diff(first, second)).rstrip('\n')
    #return plain(rekursive_diff(first, second)).rstrip('\n')
    return first, second
        
def rekursive_diff(first: Union[JsonObject, YamlObject], second: Union[JsonObject, YamlObject]) -> dict[str, Union[dict, str, int, bool]]:
    if type(first) is dict and type(second) is dict:
        keys_all = list(first.keys()) + list(second.keys())
    elif type(first) is dict and type(second) is not dict:
        keys_all = list(first.keys())
    else:
        keys_all = list(second.keys())
    keys_all = set(keys_all)
    keys_all = list(keys_all)
    keys_all.sort()
    result_dict = {
        
    }
    for key in keys_all:
        if key in first and key not in second:
            result_dict[key] = ['deleted', first[key]]
        elif key not in first and key in second:
            result_dict[key] = ['added', second[key]]
        elif isinstance(first.get(key), dict) and isinstance(second.get(key), dict):
            result_dict[key] = ['recursiv', rekursive_diff(first.get(key), second.get(key))]
        elif key in first and key in second:
            if first[key] == second[key]:
                result_dict[key] = ['unchanged', first[key]]
            elif first[key] != second[key]:
                result_dict[key] = ['changed', first[key], second[key]]
    return result_dict


def choise_format(format: str, first: dict, second: dict):
    if format == 'plain':
        return plain(rekursive_diff(first, second)).rstrip('\n')
    if format == 'stylish':
        return formater(0, rekursive_diff(first, second)).rstrip('\n')