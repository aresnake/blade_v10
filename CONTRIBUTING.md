# Contributing (Blade v10/v11)

## Branches
- main: stable uniquement (protégée)
- v10-dev: intégration v11 (PR requises)
- feat/intent-...: 1 intent = 1 branche + 1 PR

## PR
- Toujours en draft jusqu’à ce que l’implémentation soit prête
- Utiliser le template PR
- DoD commun: data API (no-ops), réfs explicites, FixBook si besoin, logs, 1 test OK + 1 test correction

## Tests
- YAML dans tests/
- Runner (à venir) déposera les artefacts dans out/ et les logs dans logs/
