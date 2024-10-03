import pytest
import json
from gendiff.scripts.gendiff import choise_format
import yaml
from yaml.loader import SafeLoader


def test_choise_format():
    format = 'plain'
    first = json.load(open('tests/fixtures/file1.json'))
    second = json.load(open('tests/fixtures/file2.json'))
    result = open('tests/fixtures/plain.txt').read()

    assert choise_format(format, first, second) == result

    first = yaml.load(open('tests/fixtures/file1.yaml'), Loader=SafeLoader)
    second = yaml.load(open('tests/fixtures/file2.yaml'), Loader=SafeLoader)

    assert choise_format(format, first, second) == result

    format = 'stylish'

    first = json.load(open('tests/fixtures/file1.json'))
    second = json.load(open('tests/fixtures/file2.json'))
    result = open('tests/fixtures/result.txt').read()
    assert choise_format(format, first, second) == result

    first = yaml.load(open('tests/fixtures/file1.yaml'), Loader=SafeLoader)
    second = yaml.load(open('tests/fixtures/file2.yaml'), Loader=SafeLoader)

    assert choise_format(format, first, second) == result

