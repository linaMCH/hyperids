# Paramètres communs aux deux membres du binôme.
# Toute modification doit être discutée et poussée via une pull request.

SEED = 42  # graine aléatoire unique pour tout le projet

# À fixer ensemble avant de lancer les expériences :
# TEST_SIZE = ...
# N_TRIALS = ...   # budget d'essais identique pour chaque méthode d'optimisation

# Attention : dans les fichiers d'origine, les noms sont inversés par rapport à la
# description des auteurs.
# 'UNSW_NB15_testing-set.csv'  : 175 341 lignes = partition d'ENTRAINEMENT officielle
# 'UNSW_NB15_training-set.csv' : 82 332 lignes  = partition de TEST officielle
TRAIN_FILE = 'UNSW_NB15_testing-set.csv'
TEST_FILE = 'UNSW_NB15_training-set.csv'