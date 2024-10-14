from typing import Union


BASE_TAB = "    "


def formater(
        depth, result_dict: dict[str, Union[dict, str, int, bool, list]]
) -> str:
    result = "{" + "\n"
    tab = "    " * depth
    for key, value in result_dict.items():
        match value[0]:
            case "deleted":
                result += f"{tab}  - {key}: {value_to_json(value[1], tab)}\n"
            case "added":
                result += f"{tab}  + {key}: {value_to_json(value[1], tab)}\n"
            case "recursiv":
                result += f"{tab}    {key}: {formater(depth+1, (value[1]))}"
            case "unchanged":
                result += f"{tab}    {key}: {value_to_json(value[1], tab)}\n"
            case "changed":
                result += f"{tab}  - {key}: {value_to_json(value[1], tab)}\n"
                result += f"{tab}  + {key}: {value_to_json(value[2], tab)}\n"
    return result + tab + "}" + "\n"


def value_to_json(value: bool | None | int | str | dict, tab):
    if type(value) is bool:
        result = str(value)
        result = result.lower()
        return result
    if value is None:
        return "null"
    if type(value) is dict:
        result = "{" + "\n"
        for ke, val in value.items():
            if type(val) is dict:
                val = value_to_json(val, tab + BASE_TAB)
            result += f"{BASE_TAB}{tab}    {ke}: {val}\n"
        return result + tab + BASE_TAB + "}"
    else:
        return value
