from pathlib import Path

from requests.sessions import Session
import typer

from crackmes_dl.endpoints import CrackmeEndpoint
from crackmes_dl.endpoints import LoginEndpoint
from crackmes_dl.endpoints import SearchEndpoint
from crackmes_dl.payloads import AuthPayload
from crackmes_dl.payloads import SearchPayload
from crackmes_dl.responses import SearchResultEntry


class CrackmesApi:
    def __init__(self, domain: str) -> None:
        self._session = Session()
        self._login = LoginEndpoint(domain=domain)
        self._search = SearchEndpoint(domain=domain)
        self._crackme = CrackmeEndpoint(domain=domain)

    def login(self, payload: AuthPayload) -> bool:
        return self._login.authenticate(session=self._session, payload=payload)

    def search(self, payload: SearchPayload) -> list[SearchResultEntry]:
        return self._search.search(session=self._session, payload=payload)

    def download(self, output_dir: Path, crackmes: list[SearchResultEntry]) -> None:
        with typer.progressbar(crackmes, label=f"Downloading {len(crackmes)} crackmes") as progress:
            for crackme in progress:
                self._crackme.download(
                    session=self._session,
                    crackme=crackme.crackme,
                    output_dir=output_dir,
                )
