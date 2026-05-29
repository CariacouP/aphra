# /project-init

**Description:** Initialise l'équipe d'agents dans un nouveau projet ou un projet existant, et prépare le Backlog et la Vision avant de démarrer les Sprints.

**Étapes:**
1. **Bootstrap** (@scrum-master) : Vérifie l'existence du dossier `.agents/scrum_artifacts/` et de `skills/vision.md`. S'ils n'existent pas, il crée l'arborescence et les fichiers modèles (Sprint_Board, Blockers, Dette_UI_Backlog, Product_Backlog, Personas, vision.md).
2. **Audit & Cleanup** (@po et @ba) : 
   - Si le projet contient déjà du code ou de la documentation existante, les agents scannent le projet pour comprendre l'architecture et les fonctionnalités actuelles.
   - **Important :** S'il existe déjà des documents de vision, de personas ou de roadmap dans le projet d'origine, l'équipe s'en inspire fortement pour remplir ses propres modèles dans `.agents/scrum_artifacts/` et `skills/vision.md`. Une fois le contenu migré dans nos templates pour garder la standardisation, les anciens documents de vision/roadmap de la racine doivent être **supprimés** pour garder le projet propre et sans redondances.
   - @po et @ba rédigent un premier brouillon de la vision, des Personas, et du Product Backlog.
3. **Interview Sponsor** (@po) : Le Product Owner utilise explicitement la commande `/grill-me` avec le Sponsor (l'utilisateur humain) pour s'aligner sur la vision, valider les Personas, et prioriser les prochaines grandes étapes du Backlog de manière interactive.
4. **Ready** (@scrum-master) : Une fois l'interview terminée et les artefacts de base validés par le Sponsor, l'équipe est officiellement onboardée. Le Scrum Master indique que l'utilisateur peut maintenant lancer `/jules-auto` ou `/sprint-planning` pour commencer le développement.
