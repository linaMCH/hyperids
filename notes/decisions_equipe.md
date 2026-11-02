# Journal des décisions de l'équipe

Chaque décision est notée avec sa date, sa raison et les alternatives écartées,
pour pouvoir la justifier dans le rapport.

| Date | Décision | Raison | Alternatives écartées | Statut |
|---|---|---|---|---|
| 31/10/2026 | Contexte : détection d'intrusions réseau | Sujet bien balisé, retour possible d'un professionnel de la cybersécurité | Maintenance prédictive (séries temporelles, plus lourd à mener pour un premier projet) | Décidé par Lina |
| 31/10/2026 | Dataset : UNSW-NB15 | Plus récent que KDD, taille raisonnable, partition officielle fournie | CIC-IDS2017 (plus lourd, défauts de labellisation connus [à sourcer]) | Décidé par Lina |
| 31/10/2026 | Environnement : Kaggle Notebooks (CPU) | Pas d'installation, données directement disponibles | Google Colab, ordinateur local | Décidé par Lina |
| 01/11/2026 | Tâche principale : classification binaire sur `label` | Correspond à l'énoncé ; le multiclasse reste optionnel | Classification sur `attack_cat` | Décidé par Lina |
| 01/11/2026 | `attack_cat` exclue des caractéristiques | Elle contient la réponse (fuite de données) | | Décidé par Lina |
| 01/11/2026 | Partitions utilisées selon leur contenu, pas leur nom | Noms de fichiers inversés dans cette version | | Décidé par Lina |
| 01/11/2026 | Doublons supprimés avant tout découpage | 74 301 doublons sur 175 341 lignes (42,4 %) ; fuite entre apprentissage et validation, scores gonflés | Les conserver (comparabilité avec des travaux utilisant la partition brute) | Décidé par Lina |
| 01/11/2026 | Groupes à étiquettes contradictoires supprimés (940 lignes, 229 groupes) | Cas inapprenables ; garder une ligne au hasard serait arbitraire | Garder la première ligne rencontrée | Décidé par Lina |
| 01/11/2026 | Colonnes retirées : `id`, `ct_ftp_cmd` | Identifiant ; `ct_ftp_cmd` identique à `is_ftp_login` | | Décidé par Lina |
| 02/11/2026 | Variables `proto`, `service`, `state` : une modalité est conservée si elle compte au moins 100 lignes dans l'entraînement (`train_fit`), sinon regroupée en « autres » (remplace la décision du 01/11 sur proto) | Après nettoyage, les protocoles de rang 6 à 10 n'ont que 11 à 47 lignes : catégories trop petites pour être fiables. Règle identique pour les trois colonnes | 10 protocoles les plus fréquents (justifiée par un chiffre calculé avant nettoyage) ; une colonne par valeur (133) | Décidé par Lina |
| 01/11/2026 | Test officiel nettoyé de la même façon, lignes identiques à l'entraînement retirées | Éviter qu'une ligne du test ait déjà été vue à l'entraînement | Test brut | Décidé par Lina |
| 01/11/2026 | Expériences complémentaires prévues : avec et sans doublons ; avec et sans `proto` | Mesurer l'effet des doublons et la dépendance au protocole | | Prévu |
| 02/11/2026 | Découpage entraînement / validation : 80 % / 20 %, stratifié sur `attack_cat`, SEED = 42 | Conserver les types d'attaque rares (Worms, Backdoor) dans les deux parties ; reproductibilité | Découpage aléatoire simple | Décidé par Lina |
| 02/11/2026 | Encodage one-hot de `proto`, `service`, `state` (20 colonnes) ; normalisation faite plus tard dans les pipelines des modèles qui en ont besoin | Les arbres n'ont pas besoin de normalisation ; la calculer dans le pipeline garantit qu'elle l'est sur l'entraînement uniquement | Normaliser dans le notebook de préparation (risque de fuite) | Décidé par Lina |
| 02/11/2026 | Préparation reproduite par `src/data.py` (copié dans la première cellule de chaque notebook Kaggle) et contrôlée par des empreintes ; pas de partage de fichiers de données | Pas de données dans le dépôt ; même résultat grâce à SEED = 42 ; contrôle d'identité entre les deux membres | Partager les CSV préparés (dépôt lourd, versions divergentes) | Décidé par Lina |
| 02/11/2026 | README réduit à l'objectif du projet ; rédaction complète à la fin | Décision de Lina : le rédiger en fin de projet | Garder le README détaillé | Décidé par Lina |
| 02/11/2026 | Proposition : étendre l'expérience « avec et sans `proto` » à « avec et sans variables catégorielles » ; tester stcpb et dtcpb avec et sans | Taux d'attaque très marqués pour certaines modalités (pop3 99,8 %, ssh 0,9 %, CON 3,8 %) ; stcpb et dtcpb non étudiées | | À valider |