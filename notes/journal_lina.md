# Journal de bord : Lina

Règle : une entrée par séance de travail, écrite juste après (5 à 10 minutes).
On note les chiffres exacts, les erreurs et les résultats décevants autant que les
réussites. Ce fichier est la source du rapport.

## Modèle d'entrée

### [date] : [étape], [notebook ou fichier concerné]
- **Objectif de la séance :**
- **Observé (avec chiffres) :**
- **Retenu / décidé, et pourquoi :**
- **Alternatives écartées :**
- **Problèmes rencontrés et solution :**
- **À vérifier / questions :**
- **Pour le rapport (section concernée) :**

---

### [date] : Étape 1, choix et compréhension du dataset (notebook 01_exploration)
- **Objectif :** choisir le dataset et vérifier qu'il est exploitable.
- **Observé :**
  - Version Kaggle : unsw-nb15, publiée par mrwellsdavid. Fichiers présents : training-set, testing-set, quatre fichiers bruts, description des colonnes, liste des événements. Le fichier de vérité terrain cité par les auteurs est absent de cette version.
  - Les noms des fichiers sont inversés par rapport à la description des auteurs : `UNSW_NB15_testing-set.csv` contient 175 341 lignes (partition d'entraînement officielle), `UNSW_NB15_training-set.csv` en contient 82 332 (partition de test officielle).
  - Partition d'entraînement : 56 000 normales, 119 341 attaques (68,1 % d'attaques). Partition de test : 37 000 normales, 45 332 attaques.
- **Retenu :** utiliser les partitions selon leur contenu, pas leur nom. Noms notés dans `src/config.py` et dans le README.
- **Problèmes rencontrés :** la vérification du numéro de téléphone Kaggle a échoué (demande de vérification d'identité). Non nécessaire pour la suite, car les bibliothèques utiles sont déjà installées.
- **Pour le rapport :** section Données.

### [date] : Étape 2, exploration de la partition d'entraînement (notebook 01_exploration)
- **Observé :**
  - 175 341 lignes, 45 colonnes, aucune valeur manquante.
  - 67 601 doublons hors colonne `id`, soit environ 38,6 % des lignes. Mesure détaillée à faire (répartition par classe, étiquettes contradictoires).
  - Variables de type texte : `proto` (133 valeurs), `service` (13 valeurs, dont `-` pour plus de la moitié des lignes, qui signifie service non identifié), `state` (9 valeurs).
  - Distributions très étirées sur les colonnes de volume (par exemple `sbytes` : médiane 430, maximum supérieur à 12 millions).
  - `is_ftp_login` et `ct_ftp_cmd` ont la même moyenne et le même écart-type (probablement identiques). `is_ftp_login` atteint la valeur 4 alors qu'elle devrait être binaire.
  - `attack_cat` détermine exactement `label` (Normal = 0, tout le reste = 1).
  - Types d'attaques très inégaux : 130 Worms contre 40 000 Generic.
- **Retenu :** ne jamais utiliser `attack_cat` comme caractéristique. Retirer `id`. Traiter les doublons avant tout découpage.
- **À vérifier :** doublons par classe, étiquettes contradictoires, doublons entre entraînement et test, identité de `is_ftp_login` et `ct_ftp_cmd`, utilité de `stcpb` et `dtcpb`.
- **Pour le rapport :** sections Données et Méthodes (préparation).