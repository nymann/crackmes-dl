# Crackmes DL

Download crackmes from <https://crackmes.one> using the commandline.

## Install

Requires [python3 (version >= 3.9)](https://www.python.org/downloads/) and pip

```sh
pip install --user git+https://github.com/nymann/crackmes_dl.git
```

## Usage

crackmes_dl supports three commands, you can figure this out by calling `crackmes_dl --help`.

### Download all

Given an output directory and a starting page (defaults to 1), download all crackmes that doesn't exists in the output directory.

```txt
$ crackmes_dl download-all --help
Usage: crackmes_dl download-all [OPTIONS]

Options:
  --output-dir PATH        [required]
  --domain TEXT            [default: https://crackmes.one]
  --starting-page INTEGER  [default: 1]
  --help                   Show this message and exit.
```

### Search and download

Download only crackmes matching certain filters (as seen on <https://crackmes.one/search>).
Note that using search and download without the `--no-quick` flag you can maximum download 50 crackmes at a time, this is due to a site restriction.

```txt
$ crackmes_dl search-and-download --help
Usage: crackmes_dl search-and-download [OPTIONS]

Options:
  --output-dir PATH               [required]
  --domain TEXT                   [default: https://crackmes.one]
  --quick / --no-quick            Faster but limited to max 50 results
                                  [default: quick]
  --name TEXT                     Name of the crackme must include 'search
                                  string'
  --author TEXT                   Author name must include 'search string'
  --difficulty-min INTEGER        Difficulty greater or equal to.  [default:
                                  1]
  --difficulty-max INTEGER        Difficulty less or equal to.  [default: 6]
  --quality-min INTEGER           Quality greater or equal to.  [default: 1]
  --quality-max INTEGER           Quality less or equal to.  [default: 6]
  --lang [C/C++|Assembler|Java|(Visual) Basic|Borland Delphi|Turbo Pascal|.NET|Unspecified/other]
                                  Defaults to including all
  --arch [x86|X86-64|java|ARM|MIPS|other]
                                  Defaults to including all
  --platform [DOS|Mac OS X|Multiplatform|Unix/linux etc.|Windows|Windows 2000/XP only|Windows 7 Only|Windows Vista Only|Unspecificed/other]
                                  Defaults to including all
  --help                          Show this message and exit.
```

### Download

Download a single crackme given a `crackme_id`. This is probably only useful for scripts.

```txt
$ crackmes_dl download --help
Usage: crackmes_dl download [OPTIONS]

Options:
  --output-dir PATH  [required]
  --crackme TEXT     fx: 617965c733c5d4329c345330  [required]
  --domain TEXT      [default: https://crackmes.one]
  --help             Show this message and exit.
```

## Development

For help getting started developing check [DEVELOPMENT.md](DEVELOPMENT.md)
