"""Préparation des données UNSW-NB15 (projet HyperIDS).

Reproduit le notebook 02_preparation. Usage :

    train, val, test, x_cols = load_prepared()
    verify(train, val, test)

Sur Kaggle, copier le contenu de ce fichier dans la première cellule de code
du notebook (les notebooks n'importent pas src/ directement).
Les noms des fichiers du dataset sont inversés dans la version Kaggle utilisée.
"""
import hashlib

import pandas as pd
from sklearn.model_selection import train_test_split

SEED = 42
BASE = '/kaggle/input/datasets/mrwellsdavid/unsw-nb15/'
TRAIN_FILE = 'UNSW_NB15_testing-set.csv'   # 175 341 lignes : entraînement officiel
TEST_FILE = 'UNSW_NB15_training-set.csv'   # 82 332 lignes : test officiel

TARGET = 'label'
DROP_COLS = ['id', 'attack_cat', 'ct_ftp_cmd']
CAT_COLS = ['proto', 'service', 'state']
MIN_COUNT = 100
VAL_SIZE = 0.2

EXPECTED = {'train': 'fb8d73b1cdba', 'val': 'f5db41df66c1', 'test': '0f96e3a31bcc'}


def _clean(df, feats):
    """Retire les groupes à étiquettes contradictoires, puis les doublons."""
    n_labels = df.groupby(feats)[TARGET].transform('nunique')
    df = df[n_labels == 1]
    df = df.drop_duplicates(subset=feats, keep='first')
    return df.reset_index(drop=True)


def _encode(df):
    df = df.drop(columns=['id', 'ct_ftp_cmd'])
    return pd.get_dummies(df, columns=CAT_COLS, dtype=int)


def load_prepared(base=BASE):
    """Retourne (train, val, test, x_cols). attack_cat reste dans les tableaux
    mais ne fait pas partie des caractéristiques (x_cols)."""
    train_raw = pd.read_csv(base + TRAIN_FILE)
    test_raw = pd.read_csv(base + TEST_FILE)
    feats = [c for c in train_raw.columns if c not in DROP_COLS + [TARGET]]

    train = _clean(train_raw, feats)
    test = _clean(test_raw, feats)

    # retire du test les lignes déjà présentes dans l'entraînement
    m = test.merge(train[feats].drop_duplicates(), on=feats, how='left', indicator=True)
    assert len(m) == len(test)
    overlap = (m['_merge'] == 'both').to_numpy()
    test = test[~overlap].reset_index(drop=True)

    # découpage entraînement / validation, stratifié sur attack_cat
    train_fit, val = train_test_split(
        train, test_size=VAL_SIZE, stratify=train['attack_cat'], random_state=SEED
    )
    train_fit = train_fit.reset_index(drop=True)
    val = val.reset_index(drop=True)

    # modalités conservées : au moins MIN_COUNT lignes dans train_fit
    keep = {}
    for c in CAT_COLS:
        vc = train_fit[c].value_counts()
        keep[c] = vc[vc >= MIN_COUNT].index.tolist()

    def group_rare(df):
        df = df.copy()
        for c in CAT_COLS:
            df[c] = df[c].where(df[c].isin(keep[c]), 'autres')
        return df

    train_fit, val, test = group_rare(train_fit), group_rare(val), group_rare(test)

    train_enc = _encode(train_fit)
    val_enc = _encode(val).reindex(columns=train_enc.columns, fill_value=0)
    test_enc = _encode(test).reindex(columns=train_enc.columns, fill_value=0)

    x_cols = [c for c in train_enc.columns if c not in (TARGET, 'attack_cat')]
    return train_enc, val_enc, test_enc, x_cols


def fingerprint(df):
    h = pd.util.hash_pandas_object(df, index=False).values
    return hashlib.md5(h.tobytes()).hexdigest()[:12]


def verify(train, val, test):
    """Compare les empreintes à celles du notebook 02_preparation."""
    got = {'train': fingerprint(train), 'val': fingerprint(val), 'test': fingerprint(test)}
    for k in got:
        statut = 'OK' if got[k] == EXPECTED[k] else 'DIFFÉRENTE'
        print(f'{k:5s} attendue {EXPECTED[k]} | obtenue {got[k]} | {statut}')
    return got == EXPECTED