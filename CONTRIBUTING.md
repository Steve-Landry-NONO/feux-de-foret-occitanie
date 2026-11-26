# Contribuer
1. Accepter les invitations Drive, Trello et GitHub (tickets #19–#24). Vérifier soi-même les accès.
2. Installer Git, cloner le dépôt et configurer son identité :
```sh
git clone https://github.com/Steve-Landry-NONO/feux-de-foret-occitanie.git
cd feux-de-foret-occitanie
git config user.name "Prénom Nom"
git config user.email "Votre adresse GitHub ou noreply"
git status
```
3. Lire AGENTS.md et le ticket, vérifier que le répertoire est propre, puis synchroniser main : `git switch main`, `git pull --ff-only`. Créer une branche dédiée, par exemple `git switch -c docs/14-regles-qualite`. Pour travailler sur une PR existante, convenir de la branche avec son auteur.
4. Produire un travail personnel expliqué, tester, inspecter `git diff`, sélectionner les fichiers explicitement, committer en français et pousser sa branche.
5. Ouvrir une PR vers main avec le numéro du ticket, les critères, preuves, limites et relecteur métier. Utiliser Closes #N seulement si tous les critères sont satisfaits ; sinon Refs #N.
6. Revue humaine distincte de l'auteur ; résoudre les conflits sans écraser les contributions. Fusion par une personne autorisée après validation.
## Terminé
Critères satisfaits, preuves et tests reproductibles, sources/licences vérifiées, décisions et glossaire actualisés si nécessaire, revue humaine, fusion et clôture. Un test non exécuté est déclaré tel quel.
