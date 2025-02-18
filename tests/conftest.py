import pathlib
import re

import pytest
import responses

from krypto.todo import Todo

sample_config = {
    "prefix": "TODO",
    "attach-issue": False,
    "include": "tests",
    "dry": True,
}

raw_todo = """
# TODO[Enhancement, Bug]: This is a sample title
# this is the body of the todo
""".strip()

username = "antoniouaa"
repository = "krypto"
url = "https://api.github.com/repos/antoniouaa/krypto/issues"

todo_from_json = [
    {
        "title": "This is a sample title",
        "body": "this is the body of the todo",
        "number": 1,
        "labels": [{"name": "Enhancement"}, {"name": "Bug"}],
        "state": "open",
    },
    {
        "title": "This is a second sample title",
        "body": "this is the body of the todo",
        "number": 2,
        "labels": [{"name": "Enhancement"}, {"name": "Bug"}],
        "state": "open",
    },
    {
        "title": "This is a final sample title",
        "body": "this is the body of the todo",
        "number": 3,
        "labels": [{"name": "Bug"}],
        "state": "closed",
    },
]

headers = {"Accept": "application/vnd.github.v3+json", "Authorization": "token abc"}


@pytest.fixture(scope="function")
def mocked_requests():
    with responses.RequestsMock() as test_session:
        yield test_session


@pytest.fixture(scope="function")
def sample_todo(tmp_path):
    info = {
        "title": "This is a sample title",
        "body": "this is the body of the todo",
        "labels": ["Enhancement", "Bug"],
        "line_no": 1,
        "origin": "test/sample_todo.py",
    }
    return Todo(**info)


@pytest.fixture(scope="function")
def req_no_body():
    issue_body = "Autogenerated by [antoniouaa/krypto](https://github.com/antoniouaa/krypto)\n\nLine: 1 in [`tests/conftest.py`](https://github.com/antoniouaa/krypto/blob/master/tests/conftest.py#L1)"
    return {"title": "This is a sample title", "body": issue_body, "labels": ["Bug"]}


@pytest.fixture(scope="function")
def mock_requests():
    with responses.RequestsMock() as mocked:
        yield mocked
