# /qa-review

**Description:** Lance la phase de test et de validation de la tâche "En Revue".

**Étapes:**
1. @qa : Analyse le code produit pour la tâche "En Revue" dans le `.agents/scrum_artifacts/Sprint_Board.md`. Il effectue une revue **purement technique** : vérifie la logique, traque les bugs, et s'assure que rien n'a été cassé.
2. @po : Vérifie que la fonctionnalité développée correspond bien aux critères d'acceptation initiaux au niveau des spécifications.
3. @scrum-master : 
   - Si des problèmes techniques sont détectés, la tâche retourne "En Cours" avec des instructions pour les développeurs.
   - Si la validation technique est réussie, la tâche reste "En Revue" et le Scrum Master DOIT lancer le workflow `/sprint-review` pour la validation UX/UI finale.
