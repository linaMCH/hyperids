# Optimisation des hyperparamètres pour la détection d'intrusions réseau

Projet du module Data Mining, 4e année Génie Logiciel, Université de Béjaïa.

Auteures : [Lina Maouche], [Nour El Imene Sahi]

## Objectif

Comparer plusieurs méthodes d'optimisation d'hyperparamètres (Grid Search,
Random Search, optimisation bayésienne avec Optuna et, si le temps le permet,
un algorithme génétique) pour la détection d'intrusions réseau. La comparaison
porte sur la performance, le temps de calcul et la stabilité des résultats.

## Données

Dataset : UNSW-NB15 (Moustafa et Slay, 2015).
Version Kaggle utilisée : [nom exact et lien de la page].
Les données ne sont pas versionnées dans ce dépôt : il faut les ajouter
comme entrée du notebook Kaggle.

## Structure du dépôt

- `notebooks/` : notebooks numérotés dans l'ordre d'exécution
- `src/` : code partagé (configuration, chargement et découpage des données)
- `results/` : résultats des expériences (petits fichiers CSV)
- `figures/` : graphiques utilisés dans le rapport
- `report/` : rapport

## Règles communes

- Graine aléatoire fixe : voir `src/config.py`.
- Mêmes jeux d'entraînement, de validation et de test pour tous les modèles.
- Le jeu de test n'est jamais utilisé pour choisir un modèle ou des hyperparamètres.
- Métriques : rappel, précision, F1-score, PR-AUC, MCC, temps de calcul.
- Même budget d'essais pour chaque méthode d'optimisation.
- Chaque expérience est enregistrée dans `results/`.

## Méthode de travail

- Aucun commit direct sur `main`.
- Une branche par tâche (`feat/...`, `docs/...`), fusionnée par pull request
  après relecture par l'autre membre du binôme.

## Sources

[À compléter au fil du projet : datasets, articles, bibliothèques.]