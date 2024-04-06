"""Main entry point for the CLI."""

from typing import List, Annotated, Optional
import typer
import questionary
import pyperclip
from sage.client.client import Client
from sage.client.client.api.default.complete_command_complete_command_post import sync_detailed, RankedCommandOutput

sage = typer.Typer()
client = Client("http://localhost:8000")


def generate_option(opt: RankedCommandOutput) -> str:
    """
    Generate a string representation of an option
    """
    return opt.command

@sage.command("")
def main(prompt: Annotated[Optional[str], typer.Argument()]):
    """
    Use Sage to generate a command
    """
    if not prompt:
        prompt = typer.prompt("Sage is a CLI that helps you write shell commands with team-specific context. Write a prompt below!\n> ", prompt_suffix="")

    typer.echo(f"Generating command for prompt: {prompt}\n")

    resp = sync_detailed(client=client, prompt=prompt)
    if resp.status_code != 200:
        typer.echo(f"Error: {resp.text}")
        return

    resp: List[RankedCommandOutput] = resp.parsed

    options = [
        generate_option(opt) for opt in resp
    ]

    # prompt the user to choose an option
    choice = questionary.select("Choose an option", choices=options, use_indicator=True).ask()

    if choice is None:
        typer.echo("No option selected.")
        return

    pyperclip.copy(choice)

    typer.echo("Command copied to clipboard!")

if __name__ == "__main__":
    typer.run(main)
