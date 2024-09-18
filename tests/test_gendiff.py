import pytest
import json
from gendiff import generate_dif


def test_generate_dif():
    first_file = json.load(open('tests/fixtures/file1.json'))
    second_file = json.load(open('tests/fixtures/file2.json'))
    result = open('tests/fixtures/result.txt').read()

    assert generate_dif(first_file, second_file) == result
