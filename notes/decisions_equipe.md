# Journal des décisions de l'équipe

Chaque décision est notée avec sa date, sa raison et les alternatives écartées,
pour pouvoir la justifier dans le rapport.

| Date | Décision | Raison | Alternatives écartées |
|---|---|---|---|
| [date] | Contexte : détection d'intrusions réseau | Sujet bien balisé, retour possible d'un professionnel de la cybersécurité | Maintenance prédictive (séries temporelles, plus lourd à mener pour un premier projet) |
| [date] | Dataset : UNSW-NB15 | Plus récent que KDD, taille raisonnable, partition officielle fournie | CIC-IDS2017 (plus lourd, défauts de labellisation connus) |
| [date] | Environnement : Kaggle Notebooks (CPU) | Pas d'installation, données directement disponibles | Google Colab, ordinateur local |
| [date] | Tâche principale : classification binaire sur `label` | Correspond à l'énoncé ; le multiclasse reste optionnel | Classification sur `attack_cat` |
| [date] | `attack_cat` exclue des caractéristiques | Elle contient la réponse (fuite de données) | |
| [date] | Partitions utilisées selon leur contenu, pas leur nom | Noms de fichiers inversés dans cette version | |