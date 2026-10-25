"""Affiche l'analyse de l'épisode précédent, relue depuis NotebookLM.

Sert à ne pas répéter la veille : la routine cloud ne garde rien d'un jour à
l'autre, mais chaque épisode laisse son texte comme source dans son notebook.
N'affiche rien (code 0) s'il n'existe pas encore d'épisode précédent.
"""

import asyncio
import sys
from datetime import date

from notebooklm import NotebookLMClient

PREFIXE = "Quotidien'IA"
TITRES_TEXTE = ("Analyse du jour", "Synthèse du jour")


async def main() -> int:
    async with NotebookLMClient.from_storage() as client:
        notebooks = [
            nb for nb in await client.notebooks.list()
            if nb.title.startswith(PREFIXE)
            and nb.created_at and nb.created_at.date() < date.today()
        ]
        if not notebooks:
            return 0
        veille = max(notebooks, key=lambda nb: nb.created_at)
        for src in await client.sources.list(veille.id):
            if src.title in TITRES_TEXTE:
                texte = await client.sources.get_fulltext(veille.id, src.id)
                print(f"# {veille.title}\n\n{texte.content}")
                return 0
    return 0


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
