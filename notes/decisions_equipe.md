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
| 01/11/2026 | `proto` : 10 valeurs les plus fréquentes (calculées sur l'entraînement), le reste regroupé en « autres » | Dix valeurs couvrent environ 93 % des lignes ; le groupe « autres » est à 99,7 % d'attaques | Une colonne par valeur (133 colonnes) | Décidé par Lina |
| 01/11/2026 | Test officiel nettoyé de la même façon, lignes identiques à l'entraînement retirées | Éviter qu'une ligne du test ait déjà été vue à l'entraînement | Test brut | Décidé par Lina |
| 01/11/2026 | Expériences complémentaires prévues : avec et sans doublons ; avec et sans `proto` | Mesurer l'effet des doublons et la dépendance au protocole | | Prévu |