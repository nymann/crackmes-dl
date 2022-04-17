from datetime import datetime

from bs4.element import Tag
from pydantic import BaseModel


class Link(BaseModel):
    text: str
    url: str

    @classmethod
    def from_col(cls, col: Tag) -> "Link":
        anchor_tag = col.find_all(href=True)[0]
        return cls(text=col.text.strip(), url=anchor_tag["href"])


class CrackmeEntry(BaseModel):
    crackme: Link
    author: Link
    language: str
    arch: str
    difficulty: float
    quality: float
    platform: str
    uploaded_ts: datetime
    solutions_count: int
    comments_count: int

    @classmethod
    def from_row(cls, row: Tag) -> "CrackmeEntry":
        cols: list[Tag] = row.find_all(name="td")
        crackme = Link.from_col(cols[0])
        author = Link.from_col(cols[1])
        stripped: list[str] = [col.text.strip() for col in cols]
        return cls(
            crackme=crackme,
            author=author,
            language=stripped[2],
            arch=stripped[3],
            difficulty=float(stripped[4]),
            quality=float(stripped[5]),
            platform=stripped[6],
            uploaded_ts=datetime.strptime(stripped[7], "%I:%M %p %m/%d/%Y"),
            solutions_count=int(stripped[8]),
            comments_count=int(stripped[9]),
        )
