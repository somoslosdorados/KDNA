import pytest


def test_encryption():
    with open("tests/data/test.txt", "r") as f:
        data = f.read()
    assert data == b"Hello World!"
