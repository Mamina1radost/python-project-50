from typing import Union


def value_to_plain(value: bool | None | int | str | dict):
    
    if '{' in str(value):
        return "[complex value]"

    if type(value) is int:
        return value
    if type(value) is bool:
        result = str(value)
        result = result.lower()
        return result
    if value == None:
        return 'null'
    if type(value) is str:
        return f"'{value}'"




def plain(
    result_dict: dict[str, Union[dict, str, int, bool, list]], base_key=""
) -> str:
    result = ""
    for key, value in result_dict.items():
        prefix = key if base_key == "" else f"{base_key}.{key}"
        c = ' '
        if value[0] == "added":
            result += f"Property '{prefix}' was added with value: {value_to_plain(value[1])}\n"
        if value[0] == "deleted":
            result += f"Property '{prefix}' was removed\n"
        if value[0] == "changed":
            #result += f"Property '{prefix}' was updated. From {value_to_plain(value[1])} to {value_to_plain(value[2])}\n"
            a = value_to_plain(value[1])
            b = value_to_plain(value[2])
            result += f"Property '{prefix}' was updated. From {a} to {b}\n"
            result+= f''
        if value[0] == "recursiv":
            result += plain(value[1], prefix)

    return result
