# /jules-auto

**Description:** Mode autonome de Jules. Enchaîne les workflows pour faire avancer le projet sans intervention humaine.

**Étapes:**
1. **Gestion Asynchrone des Blocages** : @scrum-master vérifie si des tâches nécessitent une intervention humaine ou rencontrent un blocage majeur. Le Scrum Master ne doit **plus jamais** arrêter complètement le workflow global. À la place, il doit isoler cette tâche (en la déplaçant dans la section "Tâches en Attente / Bloquées" du `.agents/scrum_artifacts/Sprint_Board.md`), notifier l'utilisateur de manière asynchrone, et continuer immédiatement avec la prochaine tâche disponible.
2. Ensuite, @scrum-master lit le `.agents/scrum_artifacts/Sprint_Board.md`.
3. Si le tableau "À Faire" et "En Cours" est vide, lance automatiquement `/sprint-planning`.
4. S'il y a des tâches "À Faire" mais aucune "En Cours" (qui ne soit pas bloquée), lance automatiquement `/develop-next`.
5. S'il y a des tâches "En Revue", lance automatiquement `/qa-review`, suivi immédiatement de `/sprint-review` si la validation technique est réussie.
6. Une fois qu'une action a été effectuée, recommence à l'étape 1 pour assurer une boucle continue (jusqu'à ce que tout soit "Terminé" ou en attente).
