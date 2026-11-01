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

### 31/10/2026 : Étape 1, choix et compréhension du dataset (notebook 01_exploration)
- **Objectif :** choisir le dataset et vérifier qu'il est exploitable.
- **Observé :**
  - Version Kaggle : unsw-nb15, publiée par mrwellsdavid. Fichiers présents : training-set, testing-set, quatre fichiers bruts, description des colonnes, liste des événements. Le fichier de vérité terrain cité par les auteurs est absent de cette version.
  - Les noms des fichiers sont inversés par rapport à la description des auteurs : `UNSW_NB15_testing-set.csv` contient 175 341 lignes (partition d'entraînement officielle), `UNSW_NB15_training-set.csv` en contient 82 332 (partition de test officielle).
  - Partition d'entraînement : 56 000 normales, 119 341 attaques (68,1 % d'attaques). Partition de test : 37 000 normales, 45 332 attaques.
- **Retenu :** utiliser les partitions selon leur contenu, pas leur nom. Noms notés dans `src/config.py` et dans le README.
- **Problèmes rencontrés :** la vérification du numéro de téléphone Kaggle a échoué (demande de vérification d'identité). Non nécessaire pour la suite, car les bibliothèques utiles sont déjà installées.
- **Pour le rapport :** section Données.

### 01/11/2026 : Étape 2, exploration de la partition d'entraînement (notebook 01_exploration)
- **Observé :**
  - 175 341 lignes, 45 colonnes, aucune valeur manquante.
  - 67 601 doublons exacts hors colonne `id` (caractéristiques et étiquettes identiques), soit environ 38,6 % des lignes. Mesure préliminaire, corrigée dans l'entrée suivante (74 301 sur les caractéristiques seules).
  - Variables de type texte : `proto` (133 valeurs), `service` (13 valeurs, dont `-` pour plus de la moitié des lignes, qui signifie service non identifié), `state` (9 valeurs).
  - Distributions très étirées sur les colonnes de volume (par exemple `sbytes` : médiane 430, maximum supérieur à 12 millions).
  - `is_ftp_login` et `ct_ftp_cmd` ont la même moyenne et le même écart-type (probablement identiques). `is_ftp_login` atteint la valeur 4 alors qu'elle devrait être binaire.
  - `attack_cat` détermine exactement `label` (Normal = 0, tout le reste = 1).
  - Types d'attaques très inégaux : 130 Worms contre 40 000 Generic.
- **Retenu :** ne jamais utiliser `attack_cat` comme caractéristique. Retirer `id`. Traiter les doublons avant tout découpage.
- **À vérifier :** doublons par classe, étiquettes contradictoires, doublons entre entraînement et test, identité de `is_ftp_login` et `ct_ftp_cmd`, utilité de `stcpb` et `dtcpb`.
- **Pour le rapport :** sections Données et Méthodes (préparation).

### 01/11/2026 : Étape 2 (suite), analyse des doublons (notebook 01_exploration, cellules 5 et 6)
- **Observé :**
  - 74 301 lignes en doublon sur les caractéristiques (42,4 %), contre 67 601 si l'on exige aussi la même étiquette : l'écart (environ 6 700 lignes) correspond à des caractéristiques identiques avec un label ou un attack_cat différent.
  - 70 116 doublons sont des attaques, 4 185 sont normaux. Generic : 36 076 doublons sur 40 000 lignes (90 %).
  - Après suppression : 101 040 lignes, 51,3 % normales et 48,7 % attaques. Le déséquilibre de départ (68 % d'attaques) était en grande partie dû aux doublons.
  - 229 groupes de lignes identiques ont des étiquettes contradictoires.
  - ct_ftp_cmd est identique à is_ftp_login (100 %). is_ftp_login prend les valeurs 0, 1, 2, 4 (compteur, pas indicateur).
  - proto : 5 valeurs couvrent environ 92 % des lignes. state : trois valeurs n'ont qu'une ligne.
- **Retenu :** supprimer les doublons avant le découpage, supprimer les groupes contradictoires, retirer id, attack_cat et ct_ftp_cmd, regrouper les valeurs rares de proto. décision de Lina, à présenter à Imene.
- **Alternatives écartées :** garder les doublons (fuite de données, scores gonflés).
- **À vérifier :** taux d'attaque par protocole, effet des doublons sur le score d'un modèle de référence, recouvrement entre entraînement et test.
- **Pour le rapport :** sections Données (préparation) et Discussion (comparabilité avec la littérature).

### 01/11/2026 : Étape 2 (fin), contradictions et protocoles (notebook 01_exploration, cellule 7)
- **Observé :**
  - 940 lignes (229 groupes) ont des caractéristiques identiques mais des étiquettes contradictoires : 543 Fuzzers, 396 Normal, 1 Shellcode.
  - Taux d'attaque par protocole : arp 0 %, tcp 51 %, udp 78 %, ospf 97,5 %, unas, sctp, any, gre, mobile et ipv6 100 %, valeurs rares regroupées 99,7 %.
- **Retenu :** supprimer les groupes contradictoires ; regrouper les protocoles rares en « autres ».
- **Hypothèse à tester :** le modèle s'appuie fortement sur le protocole ; possible biais de génération du trafic d'attaque. Prévoir une expérience sans `proto`.
- **Limite à écrire dans le rapport :** la suppression des contradictions retire des cas difficiles (Fuzzers ressemblant à du trafic normal).
- **À poser au professionnel de cybersécurité :** un protocole rare signale-t-il une attaque sur un vrai réseau ?
- **Pour le rapport :** sections Données, Discussion et Limites.