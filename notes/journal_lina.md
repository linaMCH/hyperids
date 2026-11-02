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
- - **Problèmes rencontrés :** la vérification du numéro de téléphone Kaggle a échoué (demande de vérification d'identité). pandas et scikit-learn fonctionnent sans installation (vérifié le 02/11/2026 dans 02_preparation). À vérifier : xgboost, lightgbm et optuna.
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

### 02/11/2026 : Étape 3, préparation et découpage (notebook 02_preparation, src/data.py)
- **Objectif :** produire des jeux d'entraînement, de validation et de test propres, sans fuite de données, reproductibles.
- **Observé :**
  - Nettoyage identique pour les deux fichiers (41 caractéristiques : 45 colonnes moins id, attack_cat, ct_ftp_cmd et label) :

    | | Départ | Sans contradictions | Sans doublons | Sans recouvrement avec l'entraînement | Variation totale |
    |---|---|---|---|---|---|
    | Entraînement | 175 341 | 174 401 (-940) | 100 811 | sans objet | -42,5 % |
    | Test | 82 332 | 82 318 (-14) | 53 940 | 52 738 (-1 202 : 757 attaques, 445 normales) | -35,9 % |

  - Part d'attaques : 48,8 % à l'entraînement (68 % avant nettoyage), 36 % au test (55 % avant nettoyage).
  - Découpage 80 % / 20 % stratifié sur attack_cat, SEED = 42 : entraînement 80 648, validation 20 163 (part d'attaques 0,488 dans les deux), test 52 738 (0,360). Aucune ligne de validation identique à une ligne d'entraînement.
  - Répartition par type :

    | Type | Entraînement | Validation | Test |
    |---|---|---|---|
    | Normal | 41 328 | 10 333 | 33 755 |
    | Exploits | 14 977 | 3 744 | 7 085 |
    | Fuzzers | 11 852 | 2 963 | 4 335 |
    | Reconnaissance | 5 138 | 1 284 | 2 224 |
    | Generic | 3 139 | 785 | 3 381 |
    | DoS | 2 403 | 601 | 1 186 |
    | Shellcode | 870 | 218 | 365 |
    | Analysis | 434 | 108 | 294 |
    | Backdoor | 410 | 103 | 70 |
    | Worms | 97 | 24 | 43 |

  - Première règle testée pour proto (10 valeurs les plus fréquentes) : les protocoles de rang 6 à 10 n'ont que 47 (sctp), 16 (any), 14 (igmp), 11 (gre) et 11 (sun-nd) lignes dans l'entraînement.
  - Règle retenue (au moins 100 lignes dans l'entraînement, sinon « autres ») :
    - proto : tcp 60 985, udp 17 909, arp 524, unas 366, ospf 163 ; autres 701 lignes (96,4 % d'attaques)
    - service : -, http, dns, smtp, ftp-data, ftp, ssh, pop3 ; autres 149 lignes (98,7 % d'attaques)
    - state : FIN, INT, CON, REQ ; autres 74 lignes (10,8 % d'attaques)
  - Taux d'attaque par modalité (entraînement après nettoyage) : proto : arp 0 %, unas 100 %, ospf 71,8 %, tcp 49,9 %, udp 43,3 % ; service : pop3 99,8 %, ssh 0,9 %, http 71,3 %, dns 33,7 %, ftp-data 22,1 %, ftp 55,6 %, smtp 68,5 %, - 44,1 % ; state : CON 3,8 %, INT 80,8 %, FIN 50,9 %, REQ 17,1 %.
  - Avant nettoyage, udp était à 78 % d'attaques et ospf à 97,5 % ; après nettoyage, 43,3 % et 71,8 %.
  - Encodage one-hot : 20 colonnes (6 proto, 9 service, 5 state), 58 caractéristiques au total (38 numériques). Tailles : (80 648, 60), (20 163, 60), (52 738, 60), colonnes `label` et `attack_cat` comprises. Aucune valeur manquante, mêmes colonnes dans les trois jeux. stcpb et dtcpb conservées.
  - Empreintes : train fb8d73b1cdba, val f5db41df66c1, test 0f96e3a31bcc. Contrôle réussi après redémarrage de la session avec load_prepared() de src/data.py (trois résultats OK).
- **Retenu :** voir les décisions du 02/11/2026 dans decisions_equipe.md.
- **Alternatives écartées :** 10 protocoles les plus fréquents (catégories trop petites après nettoyage) ; une colonne par valeur de proto (133).
- **Problèmes rencontrés :** la première cellule de regroupement (10 protocoles) a remplacé la colonne proto, y compris dans le test. Cellule supprimée, session redémarrée et préparation relancée depuis le chargement.
- **Limites pour le rapport :**
  - La part d'attaques diffère entre l'entraînement/validation (48,8 %) et le test (36 %) : précision, F1 et PR-AUC dépendent de cette proportion, donc les scores de validation et de test ne sont pas directement comparables.
  - La répartition des types d'attaque diffère aussi (Backdoor : 410 lignes à l'entraînement contre 70 au test ; Generic : 3,9 % de l'entraînement contre 6,4 % du test).
  - Le nettoyage retire 42,5 % de l'entraînement et 35,9 % du test : les scores ne sont pas directement comparables à ceux de travaux qui utilisent la partition brute. La suppression des 940 lignes contradictoires retire aussi des cas difficiles (543 Fuzzers, 396 Normal, 1 Shellcode).
- **Hypothèses à tester :**
  - Certaines modalités catégorielles suffisent presque à classer une ligne (service : pop3, ssh ; state : CON, INT ; proto : arp, unas). Possible artefact de génération du trafic.
  - Utilité de stcpb et dtcpb (avec et sans).
- **À vérifier :** disponibilité de xgboost, lightgbm et optuna sans installation ; référence dans la littérature sur les doublons d'UNSW-NB15 [à sourcer].
- **À poser au professionnel de cybersécurité :** les motifs observés par service et par état (pop3, ssh, CON, INT) reflètent-ils des attaques réelles ou un trafic généré en laboratoire ?
- **Pour le rapport :** section Données (tableaux d'effectifs, préparation), section Méthodes (découpage, encodage, règle des 100 lignes), section Limites.