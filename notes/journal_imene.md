### 06/11/2026 : Configuration et vérification des données (notebook Kaggle de test)
- **Objectif de la séance :** Configurer Git et Kaggle, cloner le dépôt, vérifier que la préparation de Lina est reproduite à l'identique sur mon compte.
- **Observé (avec chiffres) :**
  - Les trois empreintes correspondent (cellule 2, verify) : train fb8d73b1cdba, val f5db41df66c1, test 0f96e3a31bcc, puis True.
  - Tailles (cellule 3) : entraînement 80 648 lignes, validation 20 163, test 52 738 ; 58 caractéristiques.
  - Bibliothèques importées sans installation (cellule 4) : pandas 2.3.3, scikit-learn 1.6.1, xgboost 3.4.1, lightgbm 4.6.0, optuna 5.0.0.
- **Retenu / décidé, et pourquoi :** La préparation est reproductible sur mon compte (empreintes identiques) : je peux démarrer la baseline. Les versions des bibliothèques sont à citer dans le rapport (reproductibilité).
- **Alternatives écartées :** Aucune (procédure du guide suivie).
- **Problèmes rencontrés et solution :** Aucun
- **À vérifier / questions :** Relecture de 01_exploration, 02_preparation et src/data.py à faire ; décisions de la section 3 à valider avec Lina. 
- **Pour le rapport (section concernée) :** Méthodes (reproductibilité : environnement et versions).
### 06/11/2026 : Étape 4, baseline avec paramètres par défaut (notebook 03_baseline)
- **Objectif de la séance :** Mesurer 5 algorithmes avec leurs paramètres par défaut, sur la validation uniquement, pour disposer d'une référence avant l'optimisation.
- **Observé (avec chiffres) :** Source : cellules 2 à 5 de 03_baseline ; 4 cœurs CPU ; SEED = 42 ; entraînement 80 648 lignes, validation 20 163, 58 caractéristiques ; empreintes identiques à celles de Lina.

  | Modèle | Rappel | Précision | F1 | PR-AUC | MCC | F1 entraînement | Temps (s) |
  |---|---|---|---|---|---|---|---|
  | Régression logistique | 0,9759 | 0,8383 | 0,9019 | 0,9576 | 0,8040 | 0,9034 | 4,29 |
  | Arbre de décision | 0,9100 | 0,9094 | 0,9097 | 0,8714 | 0,8237 | 1,0000 | 2,70 |
  | Random Forest | 0,9488 | 0,9138 | 0,9310 | 0,9824 | 0,8635 | 1,0000 | 8,52 |
  | XGBoost | 0,9448 | 0,9172 | 0,9308 | 0,9839 | 0,8634 | 0,9546 | 1,29 |
  | LightGBM | 0,9472 | 0,9127 | 0,9296 | 0,9832 | 0,8608 | 0,9400 | 1,25 |

  - Aucun score de validation proche de 100 % (F1 maximal 0,9310, PR-AUC maximale 0,9839).
  - Random Forest, XGBoost et LightGBM sont à égalité (écarts inférieurs à 0,003 sur F1, PR-AUC et MCC) ; une seule graine, donc pas de classement possible.
  - Régression logistique : meilleur rappel, plus faible précision ; F1 entraînement (0,9034) proche du F1 validation (0,9019) : pas de surapprentissage, modèle limité.
  - Arbre et Random Forest : F1 entraînement 1,0000 contre 0,9097 et 0,9310 en validation : surapprentissage avec les paramètres par défaut.
- **Retenu / décidé, et pourquoi :** Évaluation sur la validation uniquement ; le jeu de test est supprimé de la mémoire du notebook (del test) pour ne pas pouvoir l'utiliser par erreur. Paramètres par défaut, sauf max_iter=1000 pour la régression logistique (choix préventif pour éviter un arrêt avant convergence, non testé). Normalisation dans un pipeline pour la régression logistique. n_jobs=-1 pour les modèles qui le permettent.
- **Alternatives écartées :** Évaluation sur le test (interdite par le protocole). Réglage d'hyperparamètres à ce stade (rôle des étapes suivantes).
- **Problèmes rencontrés et solution :** Aucun.
- **À vérifier / questions :** PR-AUC de l'arbre (0,8714) plus basse que celle de la régression logistique (0,9576) alors que son F1 est plus haut : probablement des probabilités presque toutes égales à 0 ou 1 [à sourcer]. Écarts entre Random Forest, XGBoost et LightGBM à confirmer avec plusieurs graines. À décider avec Lina : métrique principale d'optimisation, N_TRIALS, modèles retenus, liste des graines.
- **Pour le rapport (section concernée) :** Résultats (baseline), Méthodes (protocole d'évaluation, métriques), Limites (validation issue de la même partition que l'entraînement).