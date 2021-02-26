# [Hypermodern Python](https://cjolowicz.github.io/posts/hypermodern-python-01-setup/)
Python Best Practices guide, includes a cloned series of [Medium](https://medium.com/@cjolowicz/) posts.
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

### [Click](https://palletsprojects.com/p/click/)
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

Now install the package `poetry install` and run the console script `poetry run hypermodern-python-series` and `poetry run hypermodern-python-series --help`.

### Example: Consuming a REST API with requests

```python
# src/hypermodern_python/console.py
import textwrap

import click
import requests

from . import __version__


API_URL = "https://en.wikipedia.org/api/rest_v1/page/random/summary"


@click.command()
@click.version_option(version=__version__)
def main():
    """The hypermodern Python project."""
    with requests.get(API_URL) as response:
        response.raise_for_status()
        data = response.json()

    title = data["title"]
    extract = data["extract"]

    click.secho(title, fg="green") #i.e styled echo
    click.echo(textwrap.fill(extract))
```

- Nice use of `click` and [textwrap](https://www.geeksforgeeks.org/textwrap-text-wrapping-filling-python/)

# [Chapter 2: testing](https://cjolowicz.github.io/posts/hypermodern-python-02-testing/)
- We can use `--dev` option when we add packages, if we'd like them to run on be installed only on dev and not on production:
```bash
poetry add --dev pytest
```

- Some packages support adding their configs to the `toml` file (e.g. coverage for pytest - notice the `[toml]` addition):
```bash
poetry add --dev coverage[toml] pytest-cov
``` 

- We can now add the configs to the `.toml` file:
```ini
# pyproject.toml
[tool.coverage.paths]
source = ["src", "*/site-packages"]

[tool.coverage.run]
branch = true
source = ["hypermodern_python_series"]

[tool.coverage.report]
show_missing = true
```

- We can now run:
```bash
poetry run pytest --cov
```

- And even just:
```bash
pytest --cov
```

To file the pytest run if coverage is below a TH we use:
```ini
[tool.coverage.report]
fail_under = 100
```

# [Chapter 3: linting](https://cjolowicz.github.io/posts/hypermodern-python-03-linting/)
## Security
[Safety](https://github.com/pyupio/safety) checks the dependencies of your project for known security vulnerabilities, using a curated database of insecure Python packages.

```bash
pip install safety
```

To run it `requirements.txt` reqs have to be pinned:
```bash
safety check --file=requirements.pinned.txt --full-report
```

# [Chapter 4: typing](https://cjolowicz.github.io/posts/hypermodern-python-04-typing)
## [Data validation using Desert and Marshmallow]
[Marshmallow](https://marshmallow.readthedocs.io/) allows you to define schemas to serialize, deserialize and validate data. [Desert](https://desert.readthedocs.io/) ses the type annotations of dataclasses to generate serialization schemas for them.

1. Define a `@dataclass` (in `Python<.37` we have to `pip install dataclasses`) - we'll call it `Page`:
```python
# src/hypermodern_python/wikipedia.py
from dataclasses import dataclass


@dataclass
class Page:
    title: str
    extract: str
```

2. `desert` can generate a schema from type annotations and loads the JSON data:
```python
# Generate a schema from a dataclass.
schema = desert.schema(Page)

# Use the schema to load data.
page = schema.load(data)
```

This will raise `marshmallow.ValidationError` exception if protocol is broken.

## Rutime type checker
[Typeguard](https://github.com/agronholm/typeguard) is a runtime type checker for Python: It checks that arguments match parameter types of annotated functions as your program is being executed (and similarly for return values).

see [this](https://cjolowicz.github.io/posts/hypermodern-python-04-typing/#runtime-type-checking-with-typeguard) for an example of a type-related bug which can be caught by a runtime type checker, but is not detected by `mypy` or `pytype` because the incorrectly typed argument is loaded from JSON.

More resources:
 - https://testdriven.io/blog/python-type-checking/

# [Chapter 5: documentation](https://cjolowicz.github.io/posts/hypermodern-python-05-documentation)

## Runnable Examples in docstring
[xdoctest](https://github.com/Erotemic/xdoctest) The xdoctest package runs the examples in your docstrings and compares the actual output to the expected output as per the docstring.

```python
# src/hypermodern_python/wikipedia.py
def random_page(language: str = "en") -> Page:
    """Return a random page.
    Performs a GET request to the /page/random/summary endpoint.
    Args:
        language: The Wikipedia language edition. By default, the
            English Wikipedia is used ("en").
    Returns:
        A page resource.
    Raises:
        ClickException: The HTTP request failed or the HTTP response
            contained an invalid body.
    Example:
        >>> from hypermodern_python import wikipedia
        >>> page = wikipedia.random_page(language="en")
        >>> bool(page.title)
        True
    """
```

And here is a simple result of `xdoc` execution:
```bash
=====================================
_  _ ___  ____ ____ ___ ____ ____ ___
 \/  |  \ |  | |     |  |___ [__   |
_/\_ |__/ |__| |___  |  |___ ___]  |

=====================================

Start doctest_module('src/hypermodern_python_series/wikipedia.py')
Listing tests
gathering tests
running 1 test(s)
====== <exec> ======
* DOCTEST : src/hypermodern_python_series/wikipedia.py::random_page:0, line 42 <- wrt source file
DOCTEST SOURCE
1 >>> from hypermodern_python_series import wikipedia
2 >>> page = wikipedia.random_page(language="en")
3 >>> bool(page.title)
  True
DOCTEST STDOUT/STDERR
DOCTEST RESULT
* SUCCESS: src/hypermodern_python_series/wikipedia.py::random_page:0
====== </exec> ======
============
=== 1 passed in 0.63 seconds ===
```

# [Chapter 6: CI/CD](https://cjolowicz.github.io/posts/hypermodern-python-06-ci-cd)

## Peotry versioning
## Using [Release Drafter](https://github.com/release-drafter/release-drafter)


