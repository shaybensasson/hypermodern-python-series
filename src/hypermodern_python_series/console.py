"""Command-line interface."""
import textwrap

import click

from . import __version__, wikipedia


@click.command()
@click.option(
    "--language",
    "-l",
    default="en",
    help="Language edition of Wikipedia",
    metavar="LANG",
    show_default=True,
)
@click.version_option(version=__version__)
def main(language: str) -> None:
    """The hypermodern Python project."""
    page = wikipedia.random_page(language=language)

    click.secho(page.title, fg="green")
    click.echo(textwrap.fill(page.extract))

""" OLD """
# API_URL = "https://en.wikipedia.org/api/rest_v1/page/random/summary"
# API_URL = "about:blank"

# @click.command()
# @click.version_option(version=__version__)
# def main():
#     """The hypermodern Python project."""
#     try:
#         with requests.get(API_URL) as response:
#             response.raise_for_status()
#             return response.json()
#     except requests.RequestException as error:
#         message = str(error)
#         raise click.ClickException(message)

#     title = data["title"]
#     extract = data["extract"]

#     click.secho(title, fg="green")
#     click.echo(textwrap.fill(extract))