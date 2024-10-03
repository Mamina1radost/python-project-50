from gendiff.scripts.rekursiv import rekursive_diff
import json


def format_json(first, second):
    result = json.dumps(rekursive_diff(first, second), indent=4)
    with open(
        "/home/slava/project/python_projeckt_derevo/python-project-50/tests/fixtures/res.txt",
        "w",
    ) as file:
        file.write(result)
    return result
