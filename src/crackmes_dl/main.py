from enum import Enum
from itertools import count
from pathlib import Path
from typing import Optional

import typer

from crackmes_dl.api import CrackmesApi
from crackmes_dl.payloads import SearchPayload

app = typer.Typer()

PasswordPrompt: str = typer.Option(..., prompt=True, hide_input=True)
RequiredPath: Path = typer.Option(...)
Id: str = typer.Option(..., help="fx: 617965c733c5d4329c345330")
Domain: str = typer.Option("https://crackmes.one")


class Languages(str, Enum):
    c_cpp = "C/C++"
    asm = "Assembler"
    java = "Java"
    vb = "(Visual) Basic"
    bd = "Borland Delphi"
    tp = "Turbo Pascal"
    net = ".NET"
    other = "Unspecified/other"


class Architectures(str, Enum):
    x86 = "x86"
    x86_64 = "X86-64"
    java = "java"
    arm = "ARM"
    mips = "MIPS"
    other = "other"


class Platforms(str, Enum):
    dos = "DOS"
    mac = "Mac OS X"
    multi = "Multiplatform"
    nix = "Unix/linux etc."
    win = "Windows"
    win2000_xp = "Windows 2000/XP only"
    win7 = "Windows 7 Only"
    win_vista = "Windows Vista Only"
    other = "Unspecificed/other"


Name: str = typer.Option("", help="Name of the crackme must include 'search string'")
Author: str = typer.Option("", help="Author name must include 'search string'")
Difficulty_min: int = typer.Option(1, help="Difficulty greater or equal to.")
Difficulty_max: int = typer.Option(6, help="Difficulty less or equal to.")
Quality_min: int = typer.Option(1, help="Quality greater or equal to.")
Quality_max: int = typer.Option(6, help="Quality less or equal to.")
Lang: Optional[Languages] = typer.Option(None, help="Defaults to including all")
Arch: Optional[Architectures] = typer.Option(None, help="Defaults to including all")
Platform: Optional[Platforms] = typer.Option(None, help="Defaults to including all")
Quick: bool = typer.Option(True, help="Faster but limited to max 50 results")  # noqa: WPS425


@app.command()
def download_all(
    output_dir: Path = RequiredPath,
    domain: str = Domain,
    starting_page: int = 1,
) -> None:
    api = CrackmesApi(domain=domain)
    for page in count(start=starting_page):
        typer.echo(f"Downloading page: {page}")
        crackmes = api.lasts(page=page)
        if not crackmes:
            break
        api.download(output_dir=output_dir, crackmes=crackmes)


@app.command()
def download(output_dir: Path = RequiredPath, crackme: str = Id, domain: str = "https://crackmes.one") -> None:
    api = CrackmesApi(domain=domain)
    api.download_single(crackme_id=crackme, output_dir=output_dir)


@app.command()
def search_and_download(  # noqa: WPS211
    output_dir: Path = RequiredPath,
    domain: str = Domain,
    quick: bool = Quick,
    name: str = Name,
    author: str = Author,
    difficulty_min: int = Difficulty_min,
    difficulty_max: int = Difficulty_max,
    quality_min: int = Quality_min,
    quality_max: int = Quality_max,
    lang: Optional[Languages] = Lang,
    arch: Optional[Architectures] = Arch,
    platform: Optional[Platforms] = Platform,
) -> None:
    api = CrackmesApi(domain=domain)
    search_terms = SearchPayload(
        name=name,
        author=author,
        difficulty_min=difficulty_min,
        difficulty_max=difficulty_max,
        quality_min=quality_min,
        quality_max=quality_max,
        lang=lang,
        arch=arch,
        platform=platform,
    )
    if quick:
        crackmes = api.search(payload=search_terms)
        api.download(output_dir=output_dir, crackmes=crackmes)
    else:
        for crackme in api.unlimited_search(search_terms=search_terms):
            api.download(output_dir=output_dir, crackmes=[crackme])


if __name__ == "__main__":
    app()
