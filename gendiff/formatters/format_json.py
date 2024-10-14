from gendiff.scripts.rekursiv import generate_tree
import json


def format_json(first, second):
    result = json.dumps(generate_tree(first, second), indent=4)
    return result
