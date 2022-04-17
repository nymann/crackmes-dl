from enum import Enum
from pathlib import Path
from typing import Optional

import typer

from crackmes_dl.api import CrackmesApi
from crackmes_dl.payloads import AuthPayload
from crackmes_dl.payloads import SearchPayload

app = typer.Typer()

PasswordPrompt: str = typer.Option(..., prompt=True, hide_input=True)
RequiredPath: Path = typer.Option(...)


class Languages(str, Enum):
    c_cpp = "C/C++"
    asm = "Assembler"
    java = "Java"
    vb = "(Visual) Basic"


class Architectures(str, Enum):
    x86 = "x86"
    x86_64 = "X86-64"
    java = "java"
    arm = "ARM"


class Platforms(str, Enum):
    dos = "DOS"
    mac = "Mac OS X"
    multi = "Multiplatform"
    nix = "Unix/linux etc."


@app.command()
def download_all(
    output_dir: Path = RequiredPath,
    domain: str = "https://crackmes.one",
):
    api = CrackmesApi(domain=domain)
    api.download(output_dir=output_dir, crackmes=[])


@app.command()
def search_and_download(  # noqa: WPS211
    output_dir: Path = RequiredPath,
    domain: str = "https://crackmes.one",
    name: str = typer.Option("", help="Name of the crackme must include 'search string'"),
    author: str = typer.Option("", help="Author name must include 'search string'"),
    difficulty_min: int = typer.Option(1, help="Difficulty greater or equal to."),
    difficulty_max: int = typer.Option(6, help="Difficulty less or equal to."),
    quality_min: int = typer.Option(1, help="Quality greater or equal to."),
    quality_max: int = typer.Option(6, help="Quality less or equal to."),
    lang: Optional[Languages] = typer.Option(None, help="Defaults to including all"),
    arch: Optional[Architectures] = typer.Option(None, help="Defaults to including all"),
    platform: Optional[Platforms] = typer.Option(None, help="Defaults to including all"),
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
    crackmes = api.search(payload=search_terms)
    api.download(output_dir=output_dir, crackmes=crackmes)


if __name__ == "__main__":
    app()
