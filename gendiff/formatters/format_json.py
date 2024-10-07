from gendiff.scripts.rekursiv import generate_tree
import json


def format_json(first, second):
    result = json.dumps(generate_tree(first, second), indent=4)
    with open(
        "/home/slava/project/python_projeckt_derevo/python-project-50/tests/fixtures/res.txt",
        "w",
    ) as file:
        file.write(result)
    return result
