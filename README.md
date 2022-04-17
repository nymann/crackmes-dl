# Crackmes DL

Download crackmes from <https://crackmes.one> using the commandline.

## Install

Requires [python3 (version >= 3.9)](https://www.python.org/downloads/) and pip

```sh
pip install --user git+https://github.com/nymann/crackmes_dl.git
```

## Usage

crackmes_dl supports three commands.

### Download all

Given an output directory and a starting page (defaults to 1), download all crackmes that doesn't exists in the output directory.

### Search and download

Download only crackmes matching certain filters (as seen on <https://crackmes.one/search>).
Note that using search and download you can maximum download 50 crackmes at a time, this is due to a site restriction.

### Download

Download a single crackme given a `crackme_id`. This is probably only useful for scripts.

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
  download
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

For help getting started developing check [DEVELOPMENT.md](DEVELOPMENT.md)
