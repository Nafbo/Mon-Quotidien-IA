# Routine quotidienne Quotidien'IA

Instructions suivies chaque matin par la routine cloud Claude. Modifier ce
fichier (et le pousser sur GitHub) suffit à changer le contenu des épisodes.

## 1. Préparer l'environnement

```bash
python -m pip install -q -r requirements.txt
python -m notebooklm auth check --test --json
```

Toujours utiliser `python` (et non `pip` ou `python3` seuls) : le conteneur a
plusieurs interpréteurs et la bibliothèque doit être installée dans celui qui
lance `podcast.py`.

Si la vérification échoue (cookies Google expirés), s'arrêter là et terminer
par un message clair : « Session NotebookLM expirée : relancer
`notebooklm login` sur le PC puis mettre à jour NOTEBOOKLM_AUTH_JSON dans
l'environnement cloud. »

## 2. Choisir le contenu du jour

Thème : l'actualité de l'intelligence artificielle des dernières 24 heures,
pour un auditeur francophone curieux mais pas forcément technique.

- Rechercher sur le web les 4 à 6 actualités IA les plus marquantes du jour
  (annonces de modèles, produits, recherche, régulation, économie).
- Retenir pour chacune 1 article de référence accessible publiquement (pas de
  paywall), en privilégiant les sources fiables et variées.
- Rédiger une synthèse en français (300 à 500 mots) qui résume chaque sujet et
  explique pourquoi il compte.

## 3. Écrire `episode.json`

```json
{
  "title": "Quotidien'IA – <date du jour en toutes lettres>",
  "instructions": "Podcast en français, ton dynamique et accessible. Commencer par un sommaire rapide des sujets, puis les traiter un par un en expliquant les enjeux concrets. Conclure par le sujet à suivre dans les prochains jours.",
  "urls": ["<url 1>", "<url 2>", "..."],
  "notes": "<synthèse rédigée à l'étape 2>"
}
```

## 4. Générer le podcast

```bash
python podcast.py episode.json --format deep-dive --length default
```

La génération prend en général 5 à 15 minutes : lancer la commande avec un
délai d'attente suffisant (jusqu'à 30 minutes).

## 5. Compte rendu

Terminer par un court message listant les sujets traités et le lien
NotebookLM affiché par le script. Ne rien committer ni pousser.
