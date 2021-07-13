from dataclasses import dataclass
import datetime
from typing import List, Tuple
import pathlib


@dataclass
class Todo:
    title: str
    body: str
    line_no: int
    # created_at: datetime.datetime
    origin: pathlib.Path

    def __str__(self) -> str:
        return f"{self.title}:\n{self.body}\nIn {self.origin} - line {self.line_no}"


def process_raw_todo(todo_lines: List[Tuple[int, str]]) -> Todo:
    title = todo_lines[0]
    if len(todo_lines) > 1:
        body = "\n".join([line for _, line in todo_lines[1:]])
    else:
        body = ""
    title = title[1][len("# TODO:") :].strip()
    todo = Todo(
        title=title, body=body, line_no=title[0], origin=pathlib.Path("__file__")
    )
    return todo


def parse(raw_source: str) -> List[Todo]:
    result: List[Todo] = []

    assert raw_source, "No source code provided"

    lines = raw_source.split("\n")
    normalised_lines = [line.strip() for line in lines]

    possible = []
    start = False
    for index, line in enumerate(normalised_lines, start=1):
        if not start and line.startswith("# TODO:"):
            start = True
            possible.append((index, line))
        elif start and line.startswith("# TODO:"):
            start = False
            todo = process_raw_todo(possible)
            result.append(todo)
            todo = process_raw_todo([(index, line)])
            result.append(todo)
        elif start and line.startswith("#"):
            possible.append((index, line))
        elif start and not line.startswith("#"):
            start = False
            todo = process_raw_todo(possible)
            result.append(todo)
            possible = []

    return result
