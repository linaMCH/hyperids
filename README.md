# Optimisation des hyperparamètres pour la détection d'intrusions réseau

Projet du module Data Mining, 4e année Génie Logiciel, Université de Béjaïa.

Auteures : Lina Maouche, Nour El Imene Sahi

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

Note : les noms des fichiers `UNSW_NB15_training-set.csv` et `UNSW_NB15_testing-set.csv`
sont inversés par rapport à la description des auteurs. Le premier contient 82 332
lignes (partition de test officielle), le second 175 341 lignes (partition
d'entraînement officielle). Nous utilisons la partition selon son contenu, pas
selon son nom.

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

### Jeu de données

Moustafa, N. et Slay, J. (2015). *UNSW-NB15: a comprehensive data set for network intrusion detection systems (UNSW-NB15 network data set)*. Military Communications and Information Systems Conference (MilCIS), IEEE.

- Créé par le Cyber Range Lab de l'Australian Centre for Cyber Security (ACCS), UNSW Canberra.
- Page d'origine : https://www.unsw.adfa.edu.au/unsw-canberra-cyber/cybersecurity/ADFA-NB15-Datasets/
- Version Kaggle utilisée : dataset unsw-nb15, publiée par mrwellsdavid, [\[lien de la page\]](https://www.kaggle.com/datasets/mrwellsdavid/unsw-nb15).
- Fichiers utilisés : `UNSW_NB15_training-set.csv` et `UNSW_NB15_testing-set.csv` (partition fournie par les auteurs), ainsi que `UNSW-NB15_features.csv` pour la description des colonnes.

### Références à citer obligatoirement

Les auteurs du dataset demandent de citer ces deux articles pour tout usage du jeu de données :

1. Moustafa, N. et Slay, J. (2015). *UNSW-NB15: a comprehensive data set for network intrusion detection systems (UNSW-NB15 network data set)*. Military Communications and Information Systems Conference (MilCIS), IEEE.
2. Moustafa, N. et Slay, J. (2016). *The evaluation of Network Anomaly Detection Systems: Statistical analysis of the UNSW-NB15 dataset and the comparison with the KDD99 dataset*. Information Security Journal: A Global Perspective.

### Conditions d'utilisation

Selon la description publiée par les auteurs, l'utilisation du jeu de données est libre pour la recherche académique. Tout usage commercial doit être convenu avec les auteurs (Nour Moustafa et Jill Slay). Ce projet est un travail universitaire.

### Bibliothèques

scikit-learn, XGBoost, LightGBM, Optuna, pandas, NumPy, SciPy, Matplotlib, Seaborn.

### À compléter au fil du projet

Articles, documentations et autres sources consultés.

