# Vision du Projet & Lignes Directrices pour les Agents Scrum

Ce document est la **North Star** du projet Aphra. Il définit l'objectif final, la direction architecturale et le périmètre d'action de tous les agents autonomes qui contribuent à cette base de code. Tout agent doit s'assurer que ses actions s'alignent sur cette vision.

## 1. Objectif Global
Aphra est un agent de traduction open-source utilisant des LLMs. L'objectif est d'améliorer la qualité des traductions en utilisant un workflow multi-étapes (analyse, recherche web contextuelle, première traduction, critique et raffinement) pour produire des traductions nuancées, exactes et riches en contexte. Il s'adresse aux petits projets où engager un traducteur professionnel n'est pas possible.

## 2. Architecture & Extensibilité
Aphra repose sur une architecture orientée **workflows**. Les workflows doivent être autonomes, découplés et facilement extensibles. Le registre central gère la découverte de workflows.
**Conséquence technique :** Toute nouvelle méthode de traduction ou ajout fonctionnel (ex: nouveaux types de documents comme légal, marketing, etc.) doit être implémenté via de nouveaux workflows ou l'extension des workflows existants, sans modifier de façon destructive le noyau (core).

## 3. Périmètre d'action des Agents
Les agents doivent maintenir la qualité du code (pylint, tests, documentation) et proposer des améliorations :
- **Ingénierie :** Assurer la fiabilité des processus de traduction, la modularité et l'optimisation des prompts (gestion des LLMs via OpenRouter).
- **Frontend / Interface :** L'interface actuelle est un Gradio (gradio-demo.py) et potentiellement via CLI (aphra_runner.py). L'expérience utilisateur doit rester simple et orientée vers la traduction de documents (Markdown, texte).
- **Cyber & Qualité :** Garder le projet sécurisé (pas de fuite de clés API), garantir la compatibilité (Docker, PyPI) et maintenir des tests robustes.

## 4. Horizon Lointain
L'évolution future d'Aphra pourrait inclure :
- De nouveaux connecteurs (Ollama pour du local, bases de données spécifiques).
- L'optimisation des flux (exécution parallèle).
- Le support avancé d'autres formats de fichiers (PDF, docx, etc.) tout en préservant la mise en page.
