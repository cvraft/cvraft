import os
import pytest


FIXTURES_PATH = os.path.join(os.path.dirname(__file__), 'fixtures')


def read_fixture(file_name):
    with open(os.path.join(FIXTURES_PATH, file_name), 'r') as file:
        return file.read() 

@pytest.fixture
def input_md(case):
    return read_fixture(f"{case}.md")


@pytest.fixture
def expected_html(case):
    return read_fixture(f"{case}.txt")
