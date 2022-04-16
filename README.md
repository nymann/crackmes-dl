# Crackmes DL

Download crackmes from <https://crackmes.one> using the commandline.

### Usage

```sh
pip install --user git+https://github.com/nymann/crackmes_dl.git

crackmes_dl MyUserName --output-dir ~/.local/share/crackmes
Password:
Downloading 150 crackmes  [####################################]  100%
```

### Cross platform development

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

### Developing on Linux

#### Run helping tools automatically on file change

While the `make` targets is an okay way to run things, I find it helpful to have my tests and linter running in separate terminal windows to get continous quick feedback.

The command `ag` is from The Silver Searcher program which can be found [here](https://archlinux.org/packages/community/x86_64/the_silver_searcher/). And the `entr` program can be found [here](https://archlinux.org/packages/community/x86_64/entr/).

###### Run `unit tests` on file change automatically

```sh
alias unit="ag -l | entr -c pytest --durations=0 tests/unit_tests"
```

###### Run `flake8` on file change automatically

```sh
alias flakeit="ag -l | entr -c flake8 tests src"
```
