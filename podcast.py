"""Génère l'épisode du jour de Quotidien'IA dans NotebookLM.

Lit un fichier épisode (JSON) préparé en amont, crée un notebook dédié,
y ajoute les sources puis lance un Audio Overview en français et attend
qu'il soit prêt. Le podcast apparaît ensuite dans l'app NotebookLM du
compte Google connecté (téléphone compris) : aucun téléchargement requis.

Format du fichier épisode :
    {
      "title": "Quotidien'IA – 23 octobre 2026",
      "instructions": "Consignes pour les animateurs du podcast",
      "urls": ["https://...", "..."],
      "notes": "Texte de l'analyse du jour, ajouté comme source"
    }

Authentification : variable NOTEBOOKLM_AUTH_JSON (contenu de
storage_state.json) ou profil local créé par `notebooklm login`.
"""

import argparse
import asyncio
import json
import sys

from notebooklm import AudioFormat, AudioLength, NotebookLMClient

FORMATS = {f.name.lower().replace("_", "-"): f for f in AudioFormat}
LENGTHS = {l.name.lower(): l for l in AudioLength}


async def run(episode: dict, args: argparse.Namespace) -> int:
    async with NotebookLMClient.from_storage() as client:
        nb = await client.notebooks.create(episode["title"])
        print(f"Notebook créé : {nb.id}")

        source_ids = []
        for url in episode.get("urls", []):
            try:
                src = await client.sources.add_url(nb.id, url, wait=True, wait_timeout=180)
                source_ids.append(src.id)
                print(f"  + {url}")
            except Exception as e:  # une source illisible ne doit pas bloquer l'épisode
                print(f"  ! source ignorée {url} : {e}", file=sys.stderr)

        if episode.get("notes"):
            src = await client.sources.add_text(
                nb.id, "Analyse du jour", episode["notes"], wait=True
            )
            source_ids.append(src.id)
            print("  + analyse du jour (texte)")

        if not source_ids:
            print("Aucune source exploitable, épisode abandonné.", file=sys.stderr)
            return 1

        status = await client.artifacts.generate_audio(
            nb.id,
            language=args.language,
            instructions=episode.get("instructions"),
            audio_format=FORMATS[args.format],
            audio_length=LENGTHS[args.length],
        )
        print(f"Génération audio lancée (tâche {status.task_id}), attente…")
        final = await client.artifacts.wait_for_completion(
            nb.id, status.task_id, timeout=args.timeout
        )
        print(f"Statut final : {final.status}")
        if not final.is_complete:
            print(f"Échec de la génération : {final.error}", file=sys.stderr)
            return 1
        if args.download:
            await client.artifacts.download_audio(nb.id, args.download, final.task_id)
            print(f"Audio téléchargé : {args.download}")
        print(f"https://notebooklm.google.com/notebook/{nb.id}")
        return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("episode", help="Fichier JSON de l'épisode")
    parser.add_argument("--language", default="fr")
    parser.add_argument("--format", choices=FORMATS, default="deep-dive")
    parser.add_argument("--length", choices=LENGTHS, default="default")
    parser.add_argument("--timeout", type=float, default=1800, help="Secondes max d'attente")
    parser.add_argument("--download", metavar="CHEMIN", help="Télécharge aussi l'audio")
    args = parser.parse_args()

    with open(args.episode, encoding="utf-8") as f:
        episode = json.load(f)
    return asyncio.run(run(episode, args))


if __name__ == "__main__":
    sys.exit(main())
