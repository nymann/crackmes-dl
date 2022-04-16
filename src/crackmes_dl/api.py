from datetime import datetime
from typing import Any, Optional, Union

from bs4 import BeautifulSoup
from bs4.element import ResultSet
from bs4.element import Tag
from devtools import debug
from pydantic import BaseModel
from pydantic.fields import Field
from pydantic import root_validator
from requests.models import Response
from requests.sessions import Session


class Payload(BaseModel):
    def payload(self, token: str) -> dict[str, Union[str, int]]:
        p = self.dict(by_alias=True, exclude_none=True)
        p["token"] = token
        return p


class Endpoint:
    def __init__(self, domain: str, endpoint: str) -> None:
        self.endpoint = f"{domain}/{endpoint}"

    def post(self, session: Session, payload: Payload) -> Response:
        token: str = self._find_input_token(session=session)
        p = payload.payload(token=token)
        return session.post(url=self.endpoint, data=p)

    def _find_input_token(self, session: Session) -> str:
        response: Response = session.get(url=self.endpoint)
        soup = BeautifulSoup(markup=response.text, features="html.parser")
        found_input_tokens: ResultSet = soup.find_all(name="input", attrs={"id": "token"})
        if found_input_tokens:
            return found_input_tokens[0].get("value")
        raise Exception("Couldn't find input token")


class SearchPayload(Payload):
    name: str = ""
    author: str = ""
    difficulty_min: int = Field(default=1, ge=1, le=6, alias="difficulty-min")
    difficulty_max: int = Field(default=6, ge=1, le=6, alias="difficulty-max")
    quality_min: int = Field(default=1, ge=1, le=6, alias="quality-min")
    quality_max: int = Field(default=6, ge=1, le=6, alias="quality-max")
    lang: Optional[str] = None
    arch: Optional[str] = None
    platform: Optional[str] = None

    @root_validator
    def min_is_less_than_max(cls, values: dict) -> dict[str, Any]:
        min: int = values["difficulty_min"]
        max: int = values["difficulty_max"]
        if min >= max:
            raise ValueError("difficulty_min should be minimum be 1 less than difficulty_max")
        return values


class SearchResultEntry(BaseModel):
    name: str
    author: str
    language: str
    arch: str
    difficulty: float
    quality: float
    platform: str
    uploaded_ts: datetime
    solutions_count: int
    comments_count: int

    @classmethod
    def from_row(cls, row: Tag):
        cols = [col.text.strip() for col in row.find_all(name="td")]
        return cls(
            name=cols[0],
            author=cols[1],
            language=cols[2],
            arch=cols[3],
            difficulty=float(cols[4]),
            quality=float(cols[5]),
            platform=cols[6],
            uploaded_ts=datetime.strptime(cols[7], "%I:%M %p %m/%d/%Y"),
            solutions_count=int(cols[8]),
            comments_count=int(cols[9]),
        )


class AuthPayload(Payload):
    username: str = Field(..., alias="name")
    password: str


class LoginEndpoint(Endpoint):
    def __init__(self, domain: str) -> None:
        super().__init__(domain=domain, endpoint="login")

    def authenticate(self, session: Session, payload: AuthPayload) -> bool:
        login_response = super().post(session=session, payload=payload)
        login_response.raise_for_status()
        return "Login successful!" in login_response.text


class SearchEndpoint(Endpoint):
    def __init__(self, domain: str) -> None:
        super().__init__(domain=domain, endpoint="search")

    def search(self, session: Session, payload: SearchPayload):
        search_response = super().post(session=session, payload=payload)
        search_response.raise_for_status()
        html = search_response.text
        for entry in self._search_results(html=html):
            debug(entry)

    def _search_results(self, html: str) -> list[SearchResultEntry]:
        soup = BeautifulSoup(markup=html, features="html.parser")
        tables: ResultSet = soup.find_all(name="table", attrs={"class": "table-striped"})
        if len(tables) != 1:
            raise Exception("We didn't find exactly 1 table!")
        table = tables[0]
        body = table.find(name="tbody")
        rows = body.find_all(name="tr")
        return [SearchResultEntry.from_row(row) for row in rows]


class CrackmesApi:
    def __init__(self, domain: str) -> None:
        self._session = Session()
        self._login = LoginEndpoint(domain=domain)
        self._search = SearchEndpoint(domain=domain)

    def login(self, payload: AuthPayload) -> bool:
        return self._login.authenticate(session=self._session, payload=payload)

    def search(self, payload: SearchPayload):
        return self._search.search(session=self._session, payload=payload)
