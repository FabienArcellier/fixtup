---
id: TASK-1
title: >-
  Support de docker compose en plus de docker-compose pour les installations
  d'ubuntu plus récente dans le plugin docker
status: To Do
assignee: []
created_date: '2026-02-16 22:58'
labels:
  - docker
  - ubuntu
  - compatibility
dependencies: []
---

## Description
<!-- SECTION:DESCRIPTION:BEGIN -->
Les versions récentes d'Ubuntu utilisent la commande `docker compose` (sans tiret) au lieu de `docker-compose` (avec tiret). Le plugin docker actuel ne supporte que la version avec tiret, ce qui cause des erreurs sur les systèmes récents.

### Impacts

#### Positive
- Compatibilité avec les installations Docker modernes sur Ubuntu
- Support des versions récentes de Docker Engine

#### Negative
- Nécessite de gérer deux commandes différentes selon l'environnement

#### Further consideration
- Détecter automatiquement quelle commande est disponible
- Peut nécessiter une configuration ou une détection automatique

<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] Le plugin docker détecte automatiquement si `docker compose` ou `docker-compose` est disponible
- [ ] Le plugin utilise la commande appropriée selon la disponibilité
- [ ] Les tests couvrent les deux cas (avec et sans tiret)
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->

### Files

- src/fixtup/plugins/docker.py

<!-- SECTION:PLAN:END -->
