import pathlib
from typing import List, Tuple

import click

from krypto import token
from krypto.config import Config
from krypto.todo import gather_todos
from krypto.github import get_basename, make_requests


class IssueRunner:
    def __init__(self, path: str, cwd: str, config: dict):
        self.cwd = cwd
        self.config = config
        self.todos = gather_todos(path, config=self.config)
        username, repository = get_basename()
        self.config["username"] = username
        self.config["repository"] = repository

    def __str__(self):
        return f"Runner: cwd@{self.cwd}\n{len(self.todos)} todos"

    def run(self, token: str) -> Tuple[List[str], List[str]]:
        return make_requests(token, todos=self.todos, config=self.config)


@click.command()
@click.argument("path")
@click.option("--config", default="pyproject.toml", help="Configuration file")
@click.option("--dry", is_flag=True)
def run(path, config, dry):
    config = Config(config).parse()
    config.update({"dry": dry})
    runner = IssueRunner(path, pathlib.Path.cwd(), config=config)

    successful, failed = runner.run(token)
    click.echo("Finished creating issues!")
    if successful:
        click.echo("\nIssues successfully created/updated:")
        for title in successful:
            click.echo(f"\t- {title}")
    if failed:
        click.echo("\nSome issues have failed:")
        for title in failed:
            click.echo(f"\t- {title}")
