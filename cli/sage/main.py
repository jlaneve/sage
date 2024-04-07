"""Main entry point for the CLI."""

from typing import Annotated, Optional
import typer
import questionary
import pyperclip
from sage.client.client import Client
from sage.client.client.api.default.complete_command_complete_command_post import sync_detailed, RetrievalAndOutput
from sage.client.client.models import RankedCommandOutput

sage = typer.Typer()
client = Client("http://localhost:8000")

@sage.command("graph")
def map():
    """
    Opens the knowledge graph
    """
    typer.launch("https://atlas.nomic.ai/data/lanevejulian/nl2bash/map")

def generate_option(opt: RankedCommandOutput) -> str:
    """
    Generate a string representation of an option
    """
    return opt.command

@sage.command("ask")
def main(prompt: Annotated[Optional[str], typer.Argument()]):
    """
    Use Sage to generate a command
    """
    if not prompt:
        prompt = typer.prompt("Sage is a CLI that helps you write shell commands with team-specific context. Write a prompt below!\n> ", prompt_suffix="")

    typer.echo(f"Generating command for prompt: {prompt}\n")

    resp = sync_detailed(client=client, prompt=prompt)
    if resp.status_code != 200:
        typer.echo(f"Error: {resp}")
        return

    resp: RetrievalAndOutput = resp.parsed

    options = [
        generate_option(opt) for opt in resp.retrieved_docs
    ]

    if resp.llm_generated_code:
        # remove the potential duplicate
        if resp.llm_generated_code in options:
            options.remove(resp.llm_generated_code)

        options.insert(0, f"{resp.llm_generated_code} (recommended)")

    # prompt the user to choose an option
    choice = questionary.select("Choose an option", choices=options, use_indicator=True).ask()

    if choice is None:
        typer.echo("No option selected.")
        return

    # remove (recommended) from the choice in a safe way
    if choice.endswith(" (recommended)"):
        choice = choice[:-len(" (recommended)")]

    pyperclip.copy(choice)

    typer.echo(f"\nCommand copied to clipboard: {choice}")


if __name__ == "__main__":
    typer.run(main)
