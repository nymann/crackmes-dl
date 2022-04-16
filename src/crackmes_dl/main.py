import typer

from crackmes_dl.api import AuthPayload
from crackmes_dl.api import CrackmesApi
from crackmes_dl.api import SearchPayload

app = typer.Typer()


@app.command()
def download(username: str, password: str, domain: str = "https://crackmes.one") -> None:
    api = CrackmesApi(domain=domain)
    creds = AuthPayload(name=username, password=password)
    if not api.login(payload=creds):
        raise Exception("Login failed")
    search_terms = SearchPayload(name="ransom")
    api.search(payload=search_terms)


if __name__ == "__main__":
    app()
