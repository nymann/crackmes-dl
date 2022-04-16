from datetime import datetime

from bs4.element import Tag
from pydantic import BaseModel


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
