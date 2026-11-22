# Branche actions-test — expérience GitHub Actions (TEST, 22 nov. 2026)

Branche de test uniquement. Ne pas fusionner dans `main` sans un go
explicite de Zackary. Ne pas utiliser pour autre chose que cette expérience.

## Contenu

- `universal_v6.2.0_cohen.py` — pipeline v6.2, INCHANGÉ.
  SHA-256 : `f07567c48a5625060c6c4dd7dbed3dd2df915b5c24c91ed6e8a4b735e5ec3abf`
  (identique au fichier local et à celui du dépôt tlogNext-cancer-pdac).
- `data/pdac_tcga_fluxes_v4.csv` — TCGA-PAAD v4 réel (178 tumeurs, 12 flux).
  SHA-256 : `e7a2adaba5a0ef6858b665251d56d40a26eb9edd116370bf2c686c752213a0b0`
- `data/pdac_tcga_fluxes_v4_nul.csv` — même matrice, lignes permutées (nul, graine 42).
  SHA-256 : `895a456295d2b0553a2a62910461aedecb1aeccca59f57751c87b75ce0b97da4`
- `.github/workflows/pipeline-smoke-test.yml` — UN SEUL workflow, déclenché
  MANUELLEMENT seulement (`workflow_dispatch`), qui fait tourner v6.2 en mode
  fast sur la paire réel + nul et dépose les deux `master_results.json` en
  artefacts, pour comparaison octet à octet avec les runs locaux.

## Ce que cette branche ne fait pas

- Elle ne modifie pas `main`, ni le dépôt tlogNext-cancer-pdac, ni le livre blanc.
- Elle ne lance rien automatiquement : aucun déclenchement sur push ou pull request.
- Elle ne contient aucun binaire, aucune donnée brute (les CSV font 41 Ko chacun).

## Pour passer à l'échelle (plus tard, avec un go)

Lots de nuls : une matrice de jobs (`strategy.matrix`) sur les paires
réel/nul, artefacts par job. Dépôts publics = runners standards gratuits,
sans plafond de minutes (docs GitHub, « About billing for GitHub Actions »).
Limite : 500 Mo d'artefacts sur le plan Free — rester sur les seuls
`master_results.json`.
