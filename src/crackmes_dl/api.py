from requests.sessions import Session

from crackmes_dl.endpoints import LoginEndpoint
from crackmes_dl.endpoints import SearchEndpoint
from crackmes_dl.payloads import AuthPayload
from crackmes_dl.payloads import SearchPayload


class CrackmesApi:
    def __init__(self, domain: str) -> None:
        self._session = Session()
        self._login = LoginEndpoint(domain=domain)
        self._search = SearchEndpoint(domain=domain)

    def login(self, payload: AuthPayload) -> bool:
        return self._login.authenticate(session=self._session, payload=payload)

    def search(self, payload: SearchPayload):
        return self._search.search(session=self._session, payload=payload)
