# /develop-next

**Description:** Assigne et développe la prochaine tâche prioritaire.

**Étapes:**
1. @scrum-master : Lit `.agents/scrum_artifacts/Sprint_Board.md`, prend la tâche la plus urgente dans la colonne "À Faire" et la déplace dans "En Cours". Il s'assure que la tâche englobe l'intégration complète (Back puis Front) sauf s'il s'agit d'une pure dette technique.
2. @cyber : Analyse la tâche pour relever les précautions de sécurité à prendre selon `skills/security_rules.md`.
3. @dev-back : Développe en premier lieu l'architecture, l'API et la logique backend (si nécessaire) en respectant `skills/backend_rules.md` et les consignes de sécurité.
4. @dev-front : Développe l'interface utilisateur qui s'intègre au backend, rendant la fonctionnalité utilisable par l'utilisateur final, en respectant `skills/frontend_rules.md`.
5. **Règle d'Auto-Résolution (Self-Healing de 3 essais)** : Si un développeur (@dev-back, @dev-front, etc.) rencontre une erreur de compilation, un crash ou un test échoué pendant le développement, il n'a pas le droit de bloquer la tâche immédiatement. Il doit obligatoirement tenter de diagnostiquer et corriger l'erreur de manière autonome au moins 3 fois de suite.
6. **Gestion Asynchrone des Blocages** : Si la tâche reste bloquée après les 3 tentatives d'auto-résolution, ou si elle nécessite une intervention humaine incontournable, le développeur alerte le @scrum-master. Le Scrum Master isole alors la tâche en la déplaçant dans la section "Tâches en Attente / Bloquées" du Sprint Board, notifie l'utilisateur, et ne bloque pas le workflow : il passe à la tâche disponible suivante.
7. @scrum-master : Déplace la tâche dans "En Revue" uniquement une fois que les développements Back et Front sont terminés et fonctionnels.
