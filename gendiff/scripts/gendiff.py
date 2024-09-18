import argparse
import json
from typing import TypedDict

def main():
    parser = argparse.ArgumentParser(description='Compares two configuration files and shows a difference.')
    
    parser.add_argument('first_file')
    parser.add_argument('second_file')
    parser.add_argument('-f', '--format', help='set format of output')

    args = parser.parse_args()
    first_file = json.load(open(args.first_file))
    second_file = json.load(open(args.second_file))

    result = generate_dif(first_file, second_file)
    print(result)

class JsonObject(TypedDict):
    pass

def generate_dif(first: JsonObject, second: JsonObject) -> str:
    result = '{\n'
    keys_all = list(first.keys()) + list(second.keys())
    keys_all = set(keys_all)
    keys_all = list(keys_all)
    keys_all.sort()
    for key in keys_all:
        if key in first and key not in second:
            result += f'  - {key}: {first[key]}\n'
        elif key in first and key in second:
            if first[key] == second[key]:
                result += f'    {key}: {first[key]}\n'
            elif first[key] != second[key]:
                result += f'  - {key}: {first[key]}\n'
                result += f'  + {key}: {second[key]}\n'
        elif key not in first and key in second:
            result += f'  + {key}: {second[key]}\n'
    return result + '}'


