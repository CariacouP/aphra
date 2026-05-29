# Product Backlog

> *Ordre de priorité (de haut en bas)*

## 🚀 Sprint Actuel / MVP (Backend & Moteur de Livres)
- [ ] **Ingestion de Livres Entiers** : Implémenter le support natif des fichiers complets (EPUB, gros Markdown).
- [ ] **Découpage Automatique (Chunking)** : Ajouter un module pour découper automatiquement un livre entier par chapitres ou parties logiques pour la traduction.
- [ ] **Orchestration Flexible** : Le système doit pouvoir traduire un chapitre individuel OU orchestrer la traduction séquentielle d'un livre entier (en générant et maintenant le lorebook).
- [ ] **Optimisation Modèles Locaux (Ollama)** : Assurer la robustesse des prompts et la gestion du contexte pour éviter que les modèles locaux non censurés ne perdent le fil.

## 🌟 Fonctionnalités Futures
- [ ] **Interface Web Complète (SaaS/Local)** : Développer une interface (ex: React/Next.js) très simple et magnifique permettant l'upload de livres, le paramétrage (choix mix cloud/local) et le suivi en temps réel.
- [ ] **Déploiement Hybride (VPS/SaaS/Local)** : Packager la solution pour permettre un lancement sur VPS ou en local pur avec gestion de coûts (mix cloud/local).
- [ ] **Sélection Multi-Fournisseurs et Workflows Avancés (UI)** : Offrir un contrôle fin depuis l'interface web pour choisir le fournisseur de modèle (Ollama, OpenRouter, ou autres API personnalisées) ainsi que le workflow spécifique à utiliser, avec la possibilité de paramétrer les clés API par fournisseur.

## ✅ Terminées (Historique récent)
- [x] Architecture modulaire des workflows.
- [x] Initialisation Scrum (Sprint Board, Personas, Vision).
