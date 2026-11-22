#!/usr/bin/env python3
"""Construction d'UN nul frais — regle gelee du projet (build_nulls_893.py).

Methode exacte du lot §8.93 en cours (PROTOCOL_nulls_distribution_893.md
§3b, methode de build_nulls_n70_853.py) :
  rng = np.random.default_rng(graine)
  perm = rng.permutation(n)
  lignes entieres permutees (les flux d'une tumeur voyagent ensemble),
  colonne de controle (premiere colonne) INCHANGEE.
Assertions identiques a build_nulls_893.py : controle inchange, memes
lignes (multiset), 0 valeur manquante.

Usage :
  python3 build_null_893.py --real <csv reel> --seed <graine> --out <csv nul>
Sortie : le CSV nul, et son SHA-256 sur stdout ("SHA256 <sha> <fichier>").
Ce script est utilise DES DEUX COTES de la double piste (local et GitHub
Actions) : meme script, meme graine, meme CSV reel -> meme nul, octet a
octet. Validation faite le 22 nov. 2026 : (tcga_v4, graine 9101) reproduit
exactement le fichier du lot en cours (SHA 22f39bf7...e8fa, cf.
nulls_893_files.json) — voir README.md du lot.
"""
import argparse
import hashlib
import sys

import numpy as np
import pandas as pd


def sha(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def build_nul(src_path, seed, out_path):
    df = pd.read_csv(src_path)
    control = df.columns[0]
    rng = np.random.default_rng(seed)
    perm = rng.permutation(len(df))
    nul = df.copy()
    nul.iloc[:, 1:] = df.iloc[:, 1:].to_numpy()[perm]
    assert (nul[control].values == df[control].values).all()
    cols = [c for c in df.columns if c != control]
    assert sorted(map(tuple, nul[cols].values.tolist())) == sorted(
        map(tuple, df[cols].values.tolist()))
    assert not nul.isna().any().any()
    nul.to_csv(out_path, index=False)
    return sha(out_path)


def main():
    ap = argparse.ArgumentParser(description="Construit un nul frais (regle §8.93).")
    ap.add_argument("--real", required=True, help="CSV reel d'entree")
    ap.add_argument("--seed", required=True, type=int, help="Graine (ex. 9111)")
    ap.add_argument("--out", required=True, help="CSV nul de sortie")
    args = ap.parse_args()
    s = build_nul(args.real, args.seed, args.out)
    print(f"SHA256 {s} {args.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
