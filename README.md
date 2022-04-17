# Crackmes DL

Download crackmes from <https://crackmes.one> using the commandline.

## Install

Requires [python3 (version >= 3.9)](https://www.python.org/downloads/) and pip

```sh
pip install --user git+https://github.com/nymann/crackmes_dl.git
```

## Usage

crackmes_dl supports two commands

### Download all

Given an output directory and a starting page (defaults to 1), download all crackmes that doesn't exists in the output directory.

### Search and download

Download only crackmes matching certain filters (as seen on <https://crackmes.one/search>).
Note that using search and download you can maximum download 150 crackmes at a time, this is due to a site restriction.

### Help

#### See available commands

```sh
$ crackmes_dl --help
Usage: crackmes_dl [OPTIONS] COMMAND [ARGS]...

Options:
  --install-completion [bash|zsh|fish|powershell|pwsh]
                                  Install completion for the specified shell.
  --show-completion [bash|zsh|fish|powershell|pwsh]
                                  Show completion for the specified shell, to
                                  copy it or customize the installation.
  --help                          Show this message and exit.

Commands:
  download-all
  search-and-download
```

#### Get help for a specific command

```sh
$ crackmes_dl download-all --help
Usage: crackmes_dl download-all [OPTIONS]

Options:
  --output-dir PATH        [required]
  --domain TEXT            [default: https://crackmes.one]
  --starting-page INTEGER  [default: 1]
  --help                   Show this message and exit.
```

## Development

#### Cross platform development

By installing `make` you can do the following:

```sh
$ make help
make install
 - Installs crackmes_dl.
make install-all
 - Install crackmes_dl, all development and tests dependencies.
make test
 - Runs integration tests and unit tests
make unit-test
 - Runs integration tests
make integration-tests
 - Runs unit tests
make lint
 - Lints your code (black, flake8 and mypy).
make fix
 - Autofixes imports and some formatting.
```

#### Developing on Linux

##### Run helping tools automatically on file change

While the `make` targets is an okay way to run things, I find it helpful to have my tests and linter running in separate terminal windows to get continous quick feedback.

The command `ag` is from The Silver Searcher program which can be found [here](https://archlinux.org/packages/community/x86_64/the_silver_searcher/). And the `entr` program can be found [here](https://archlinux.org/packages/community/x86_64/entr/).

##### Run `unit tests` on file change automatically

```sh
alias unit="ag -l | entr -c pytest --durations=0 tests/unit_tests"
```

##### Run `flake8` on file change automatically

```sh
alias flakeit="ag -l | entr -c flake8 tests src"
```
