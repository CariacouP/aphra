# /sprint-planning

**Description:** Lance la planification du prochain Sprint.

**Étapes:**
1. @scrum-master : Lit le `.agents/scrum_artifacts/Product_Backlog.md` ET le `.agents/scrum_artifacts/Dette_UI_Backlog.md` et identifie les prochaines priorités (avec priorité sur la dette UI si elle existe).
2. @po : Confirme l'alignement avec `skills/vision.md` et sélectionne les éléments à inclure dans le Sprint.
3. @ba : Prend les éléments sélectionnés et les décompose en **User Stories par Persona** en se basant sur `.agents/scrum_artifacts/Personas.md`. Pour chaque fonctionnalité, il génère les User Stories associées sous la forme *"En tant que [Persona], je veux [Action] afin de [Bénéfice]"*. Il décompose ensuite ces User Stories en tâches techniques détaillées et actionnables (Front et Back).
4. @scrum-master : Met à jour `.agents/scrum_artifacts/Sprint_Board.md` dans la colonne "À Faire" avec les nouvelles User Stories et leurs tâches techniques générées par le @ba.
