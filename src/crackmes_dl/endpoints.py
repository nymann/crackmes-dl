from datetime import datetime
from io import BytesIO
import os
from pathlib import Path
from zipfile import ZipFile

from bs4 import BeautifulSoup
from bs4.element import ResultSet
from pydantic.main import BaseModel
from requests.models import Response
from requests.sessions import Session

from crackmes_dl.payloads import AuthPayload
from crackmes_dl.payloads import Payload
from crackmes_dl.payloads import SearchPayload
from crackmes_dl.responses import CrackmeEntry
from crackmes_dl.responses import Link

HTML_PARSER = "html.parser"


class Endpoint:
    def __init__(self, domain: str, endpoint: str) -> None:
        self.endpoint = domain + endpoint


class FormEndpoint(Endpoint):
    def post(self, session: Session, payload: Payload) -> Response:
        token: str = self._find_input_token(session=session)
        payload_data = payload.payload(token=token)
        return session.post(url=self.endpoint, data=payload_data)

    def _find_input_token(self, session: Session) -> str:
        response: Response = session.get(url=self.endpoint)
        soup = BeautifulSoup(markup=response.text, features=HTML_PARSER)
        found_input_tokens: ResultSet = soup.find_all(name="input", attrs={"id": "token"})
        if found_input_tokens:
            return found_input_tokens[0].get("value")
        raise Exception("Couldn't find input token")


class LoginEndpoint(FormEndpoint):
    def __init__(self, domain: str) -> None:
        super().__init__(domain=domain, endpoint="/login")

    def authenticate(self, session: Session, payload: AuthPayload) -> bool:
        login_response = self.post(session=session, payload=payload)
        login_response.raise_for_status()
        return "Login successful!" in login_response.text


class SearchEndpoint(FormEndpoint):
    def __init__(self, domain: str) -> None:
        super().__init__(domain=domain, endpoint="/search")

    def search(self, session: Session, payload: SearchPayload) -> list[CrackmeEntry]:
        search_response = self.post(session=session, payload=payload)
        search_response.raise_for_status()
        html = search_response.text
        return self._search_results(html=html)

    def _search_results(self, html: str) -> list[CrackmeEntry]:
        soup = BeautifulSoup(markup=html, features=HTML_PARSER)
        tables: ResultSet = soup.find_all(name="table", attrs={"class": "table-striped"})
        if len(tables) != 1:
            raise Exception("We didn't find exactly 1 table!")
        table = tables[0]
        body = table.find(name="tbody")
        rows = body.find_all(name="tr")
        return [CrackmeEntry.from_row(row) for row in rows]


class Metadata(BaseModel):
    crackme_url: str
    download_url: str
    author: str
    description: str
    language: str
    arch: str
    difficulty: float
    quality: float
    platform: str
    uploaded_ts: datetime

    @classmethod
    def from_html(cls, html: str, crackme_id: str, domain: str) -> "Metadata":  # noqa: WPS210
        soup = BeautifulSoup(markup=html, features=HTML_PARSER)
        section = soup.find_all(name="div", attrs={"class": "panel-background"})[0]
        p_tags = [p_tag.text.strip() for p_tag in section.find_all(name="p")]
        author: str = p_tags[0].replace("Author: ", "")
        description: str = p_tags[8]
        language: str = p_tags[1].replace("Language: ", "")
        arch: str = p_tags[6].replace("Arch: ", "")
        difficulty: float = float(p_tags[4].replace("Difficulty: ", ""))
        quality: float = float(p_tags[5].replace("Quality: ", ""))
        platform: str = p_tags[3].replace("Platform\n", "").strip()
        uploaded: str = p_tags[2].replace("Upload: ", "").strip()
        uploaded_ts: datetime = datetime.strptime(uploaded, "%I:%M %p %m/%d/%Y")

        return Metadata(
            crackme_url=f"{domain}/crackme/{crackme_id}",
            download_url=f"{domain}/static/crackme/{crackme_id}.zip",
            author=author,
            description=description,
            language=language,
            arch=arch,
            difficulty=difficulty,
            quality=quality,
            platform=platform,
            uploaded_ts=uploaded_ts,
        )


class CrackmeEndpoint(Endpoint):
    def __init__(self, domain: str) -> None:
        self.domain = domain
        super().__init__(domain=domain, endpoint="/crackme")

    def download(self, session: Session, crackme: Link, output_dir: Path) -> None:  # noqa: WPS210
        crackme_id: str = crackme.url.split("/")[-1]
        output_path = output_dir.joinpath(crackme_id)
        if self._file_already_exists(output_path=output_path):
            return
        os.makedirs(output_path)
        metadata = self._find_metadata(session=session, crackme_id=crackme_id)
        crackme_dl_response: Response = session.get(metadata.download_url)
        encrypted_zip = ZipFile(BytesIO(crackme_dl_response.content))
        pwd = b"crackmes.de" if metadata.author == "crackmes.de" else b"crackmes.one"
        encrypted_zip.extractall(path=output_path, pwd=pwd)
        with open(file=output_path.joinpath("metadata.json"), mode="w+") as json_file:
            json_file.write(metadata.json())

    def _find_metadata(self, session: Session, crackme_id: str) -> Metadata:
        response: Response = session.get(f"{self.endpoint}/{crackme_id}")
        response.raise_for_status()
        return Metadata.from_html(html=response.text, crackme_id=crackme_id, domain=self.domain)

    def _file_already_exists(self, output_path: Path) -> bool:
        return output_path.is_file()


class LastsEndpoint(Endpoint):
    def __init__(self, domain: str) -> None:
        super().__init__(domain=domain, endpoint="/lasts")

    def get_crackmes_on_page(self, session: Session, page: int) -> list[CrackmeEntry]:
        response: Response = session.get(url=f"{self.endpoint}/{page}")
        soup = BeautifulSoup(markup=response.text, features=HTML_PARSER)
        rows = soup.find_all(name="tr", attrs={"class": "text-center"})
        return [CrackmeEntry.from_row(row) for row in rows]
