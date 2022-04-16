from pathlib import Path

from bs4 import BeautifulSoup
from bs4.element import ResultSet
from requests.models import Response
from requests.sessions import Session

from crackmes_dl.payloads import AuthPayload
from crackmes_dl.payloads import Payload
from crackmes_dl.payloads import SearchPayload
from crackmes_dl.responses import Link
from crackmes_dl.responses import SearchResultEntry


class Endpoint:
    def __init__(self, domain: str, endpoint: str) -> None:
        self.endpoint = domain + endpoint

    def post(self, session: Session, payload: Payload) -> Response:
        token: str = self._find_input_token(session=session)
        payload_data = payload.payload(token=token)
        return session.post(url=self.endpoint, data=payload_data)

    def _find_input_token(self, session: Session) -> str:
        response: Response = session.get(url=self.endpoint)
        soup = BeautifulSoup(markup=response.text, features="html.parser")
        found_input_tokens: ResultSet = soup.find_all(name="input", attrs={"id": "token"})
        if found_input_tokens:
            return found_input_tokens[0].get("value")
        raise Exception("Couldn't find input token")


class LoginEndpoint(Endpoint):
    def __init__(self, domain: str) -> None:
        super().__init__(domain=domain, endpoint="/login")

    def authenticate(self, session: Session, payload: AuthPayload) -> bool:
        login_response = self.post(session=session, payload=payload)
        login_response.raise_for_status()
        return "Login successful!" in login_response.text


class SearchEndpoint(Endpoint):
    def __init__(self, domain: str) -> None:
        super().__init__(domain=domain, endpoint="/search")

    def search(self, session: Session, payload: SearchPayload) -> list[SearchResultEntry]:
        search_response = self.post(session=session, payload=payload)
        search_response.raise_for_status()
        html = search_response.text
        return self._search_results(html=html)

    def _search_results(self, html: str) -> list[SearchResultEntry]:
        soup = BeautifulSoup(markup=html, features="html.parser")
        tables: ResultSet = soup.find_all(name="table", attrs={"class": "table-striped"})
        if len(tables) != 1:
            raise Exception("We didn't find exactly 1 table!")
        table = tables[0]
        body = table.find(name="tbody")
        rows = body.find_all(name="tr")
        return [SearchResultEntry.from_row(row) for row in rows]


class CrackmeEndpoint:
    def __init__(self, domain: str) -> None:
        self.domain = domain

    def download(self, session: Session, crackme: Link, output_dir: Path) -> None:
        url = self._find_download_url(session=session, crackme=crackme)
        name = url.split("/")[-1]
        output_path = output_dir.joinpath(name)
        if self._file_already_exists(output_path=output_path):
            return
        crackme_dl_response: Response = session.get(self.domain + url)
        self._save_file(output_path=output_path, file_content=crackme_dl_response.content)

    def _find_download_url(self, session: Session, crackme: Link) -> str:
        response: Response = session.get(self.domain + crackme.url)
        response.raise_for_status()
        html = response.text
        if "btn-download" not in html:
            raise Exception("Download button not found")
        soup = BeautifulSoup(markup=html, features="html.parser")
        download_btns: ResultSet = soup.find_all(name="a", attrs={"class": "btn-download"}, href=True)
        return download_btns[0]["href"]

    def _file_already_exists(self, output_path: Path) -> bool:
        return output_path.is_file()

    def _save_file(self, output_path: Path, file_content: bytes) -> None:
        with open(file=output_path, mode="wb+") as zip_file:
            zip_file.write(file_content)
