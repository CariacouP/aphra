# /sprint-review

**Description:** Lance la réunion de revue (Sprint Review) de la tâche validée techniquement, axée sur l'Expérience Utilisateur (UX) et l'Interface.

**Étapes:**
1. @scrum-master : Déclenche le workflow pour toute tâche en "En Revue" (après validation technique par /qa-review).
2. @ux-tester : Teste la fonctionnalité d'un point de vue **strictement utilisateur**, via l'interface graphique du Frontend, en validant **chaque User Story** individuellement.
   - **Action obligatoire** : L'agent DOIT lancer l'application localement (ex: `npm run dev`) et utiliser les outils de navigation (commande `/browser` ou scripts E2E) pour interagir visuellement avec l'application. Il ne doit pas se contenter de lire le code source.
   - Pour chaque User Story, il incarne le Persona associé (Trader, Développeur Quant, etc.) tel que défini dans `.agents/scrum_artifacts/Personas.md`.
   - Il vérifie la présence du bouton/composant, son ergonomie (logique et esthétique).
   - Il vérifie que l'implémentation est de haute qualité et rapide.
   - Si une seule User Story n'est pas validée, ou si aucune interface n'existe pour une fonctionnalité Backend (hors dette technique pure), il **doit** refuser l'ensemble de la fonctionnalité.
3. @po : Valide avec le @ux-tester que la fonctionnalité globale apporte la valeur métier attendue par chaque Persona et que la Definition of Done est respectée à 100%.
4. @scrum-master : 
   - Si la revue est validée : la tâche passe en "Terminé".
   - Si des défauts UX, de lenteur, de logique, ou d'absence de Front sont constatés : @scrum-master crée une nouvelle sous-tâche prioritaire "UI Fix" liée à la User Story d'origine, et l'assigne immédiatement à @dev-front pour corriger les problèmes avant de pouvoir retenter la revue.
