import argparse
import json
import yaml
from pathlib import Path
from gendiff.schemas import JsonObject, YamlObject
from typing import Union
from yaml.loader import SafeLoader



def main():
    parser = argparse.ArgumentParser(
        description="Compares two configuration files and shows a difference."
    )

    parser.add_argument("first_file")
    parser.add_argument("second_file")
    parser.add_argument("-f", "--format", help="set format of output")


    args = parser.parse_args()
    first_file, second_file = load_json_or_yaml(args.first_file, args.second_file)

    result = generate_dif(first_file, second_file)
    print(result)


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


def generate_dif(first: Union[JsonObject, YamlObject], second: Union[JsonObject, YamlObject]) -> str:
    result = "{\n"
    keys_all = list(first.keys()) + list(second.keys())
    keys_all = set(keys_all)
    keys_all = list(keys_all)
    keys_all.sort()
    for key in keys_all:
        if key in first and key not in second:
            result += f"  - {key}: {first[key]}\n"
        elif key in first and key in second:
            if first[key] == second[key]:
                result += f"    {key}: {first[key]}\n"
            elif first[key] != second[key]:
                result += f"  - {key}: {first[key]}\n"
                result += f"  + {key}: {second[key]}\n"
        elif key not in first and key in second:
            result += f"  + {key}: {second[key]}\n"
    return result + "}"
