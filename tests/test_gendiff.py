import pytest
import json
from gendiff import generate_diff
import yaml
from yaml.loader import SafeLoader



def test_generate_diff():
    first_file = json.load(open('tests/fixtures/file1.json'))
    second_file = json.load(open('tests/fixtures/file2.json'))
    result = open('tests/fixtures/result.txt').read()

    assert generate_diff(first_file, second_file) == result

    first_file = yaml.load(open('tests/fixtures/file1.yaml'), Loader=SafeLoader)
    second_file = yaml.load(open('tests/fixtures/file2.yaml'), Loader=SafeLoader)

    assert generate_diff(first_file, second_file) == result

