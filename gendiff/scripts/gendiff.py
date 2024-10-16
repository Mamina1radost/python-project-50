import argparse
import json
import yaml
from pathlib import Path
from gendiff.schemas import JsonObject, YamlObject
from typing import Union
from yaml.loader import SafeLoader
from gendiff.formatters.stylish import formater
from gendiff.formatters.plain import plain
from gendiff.formatters.format_json import format_json
from gendiff.scripts.rekursiv import generate_tree


def main():
    parser = argparse.ArgumentParser(
        description="Compares two configuration files and shows a difference."
    )

    parser.add_argument("first_file")
    parser.add_argument("second_file")
    parser.add_argument("-f", "--format", help="set format of output")

    args = parser.parse_args()

    format = "stylish" if args.format is None else args.format
    first, second = args.first_file, args.second_file
    diff = generate_diff(first, second, format)
    print(diff)


def generate_diff(first, second, format="stylish"):
    first_file, second_file = load_json_or_yaml(first, second)

    # first, second = generate_diff(first_file, second_file)
    return choise_format(first_file, second_file, format)


def load_json_or_yaml(first, second):
    suf_first = Path(first).suffix
    suf_second = Path(second).suffix
    if suf_first == ".json":
        first_file = json.load(open(first))
    if suf_second == ".json":
        second_file = json.load(open(second))
    if suf_first == ".yaml" or suf_first == ".yml":
        first_file = yaml.load(open(first), Loader=SafeLoader)
    if suf_second == ".yaml" or suf_second == ".yml":
        second_file = yaml.load(open(second), Loader=SafeLoader)
    return first_file, second_file


def generate_diff_1(
    first: Union[JsonObject, YamlObject], second: Union[JsonObject, YamlObject]
) -> str:
    keys_all = list(first.keys()) + list(second.keys())
    keys_all = set(keys_all)
    keys_all = list(keys_all)
    keys_all.sort()
    return first, second


def choise_format(first: dict, second: dict, format: str = "stylish"):
    if format == "plain":
        return plain(generate_tree(first, second)).rstrip("\n")
    elif format == "stylish":
        return formater(0, generate_tree(first, second)).rstrip("\n")
    elif format == "json":
        return format_json(first, second)
    else:
        return "problem"
