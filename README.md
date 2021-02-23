# [Hypermodern Python](https://cjolowicz.github.io/posts/hypermodern-python-01-setup/)
---

# [Chapter 1: Setup](https://cjolowicz.github.io/posts/hypermodern-python-01-setup)
## How we actually used it:
- we skipped `pyenv`
- we created a python virtualenv with `python 3.6.9` and `pip install poetry`.
- Physically it's located in `~/NeuroHELP/Projects/MiscBestPractices/hypermodern-python-series`

## Tips
- The caret (^) in front of the version number means “up to the next **major** release”

- Use [snake case](https://en.wikipedia.org/wiki/Snake_case) for the package name hypermodern_python, as opposed to the [kebab case](https://en.wiktionary.org/wiki/kebab_case) used for the repository name hypermodern-python. In other words, name the package after your repository, replacing hyphens by underscores.

- The dependency entry in `pyproject.toml` contains a version constraint for the installed package: `click = "^7.1.2"`. This means that users of the package need to have at least the current release, `7.0`. The constraint also allows newer releases of the package, **as long as the version number does not indicate breaking changes**. (After 1.0.0, [Semantic Versioning](https://semver.org/) limits breaking changes to major releases.)

- By contrast, `poetry.lock` contains the **exact version** of `click` installed into the virtual environment. **Place this file under source control. It allows everybody in your team to work with the same environment. It also helps you keep production and development environments as similar as possible.**

- We can use `poetry update click` to update within the contraints, or `poetry add click^8.0` to upgrade to the next _major_ release.

### `Click`
- The `console` module defines a minimal command-line application, supporting `--help` and `--version` options:

```python
# src/hypermodern_python/console.py
import click

from . import __version__


@click.command()
@click.version_option(version=__version__)
def main():
    """The hypermodern Python project."""
    click.echo("Hello, world!")
```

### Going back to `Peotry`
Now install the package `poetry install` and run the console script `poetry run hypermodern-python-series` and `poetry run hypermodern-python-series --help`