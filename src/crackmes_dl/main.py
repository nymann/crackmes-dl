from pathlib import Path

import typer

from crackmes_dl.api import CrackmesApi
from crackmes_dl.payloads import AuthPayload
from crackmes_dl.payloads import SearchPayload

app = typer.Typer()

PasswordPrompt: str = typer.Option(..., prompt=True, hide_input=True)
RequiredPath: Path = typer.Option(...)


@app.command()
def download(
    username: str,
    password: str = PasswordPrompt,
    output_dir: Path = RequiredPath,
    domain: str = "https://crackmes.one",
) -> None:
    api = CrackmesApi(domain=domain)
    creds = AuthPayload(name=username, password=password)
    api.login(payload=creds)
    search_terms = SearchPayload()
    crackmes = api.search(payload=search_terms)
    api.download(output_dir=output_dir, crackmes=crackmes)


if __name__ == "__main__":
    app()
