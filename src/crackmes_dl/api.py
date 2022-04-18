import itertools
from pathlib import Path
from typing import Iterable

from requests.sessions import Session
import typer

from crackmes_dl.endpoints import CrackmeEndpoint
from crackmes_dl.endpoints import LastsEndpoint
from crackmes_dl.endpoints import LoginEndpoint
from crackmes_dl.endpoints import SearchEndpoint
from crackmes_dl.payloads import AuthPayload
from crackmes_dl.payloads import SearchPayload
from crackmes_dl.responses import CrackmeEntry
from crackmes_dl.responses import Link


class CrackmesApi:
    def __init__(self, domain: str) -> None:
        self._session = Session()
        self._login = LoginEndpoint(domain=domain)
        self._search = SearchEndpoint(domain=domain)
        self._crackme = CrackmeEndpoint(domain=domain)
        self._lasts = LastsEndpoint(domain=domain)

    def login(self, payload: AuthPayload) -> bool:
        return self._login.authenticate(session=self._session, payload=payload)

    def search(self, payload: SearchPayload) -> list[CrackmeEntry]:
        return self._search.search(session=self._session, payload=payload)

    def download_single(self, output_dir: Path, crackme_id: str) -> None:
        crackme = Link(text=crackme_id, url=f"crackme/{crackme_id}")
        self._crackme.download(
            session=self._session,
            crackme=crackme,
            output_dir=output_dir,
        )

    def download(self, output_dir: Path, crackmes: list[CrackmeEntry]) -> None:
        count = len(crackmes)
        with typer.progressbar(crackmes, label=f"Downloading {count} crackmes") as progress:
            for crackme in progress:
                self._crackme.download(
                    session=self._session,
                    crackme=crackme.crackme,
                    output_dir=output_dir,
                )

    def unlimited_search(self, search_terms: SearchPayload) -> Iterable[CrackmeEntry]:
        for page in itertools.count(start=1):
            typer.echo(f"Searching page {page}")
            crackmes_on_page = self.lasts(page=page)
            for crackme in crackmes_on_page:
                if crackme.matches_search_terms(search_terms=search_terms):
                    yield crackme
            if not crackmes_on_page:
                return

    def lasts(self, page: int) -> list[CrackmeEntry]:
        return self._lasts.get_crackmes_on_page(session=self._session, page=page)
