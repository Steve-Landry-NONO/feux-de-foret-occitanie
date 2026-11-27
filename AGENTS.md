# Instructions pour tout assistant IA
Projet pédagogique HETIC MD5, cas pédagogique SDIS 31, Occitanie. Langue de travail : français.
## Avant toute tâche
1. Identifier le ticket GitHub et son responsable réel ; lire son corps, commentaires, dépendances et PR liées. Si accès indisponible, demander les extraits nécessaires.
2. Lire README.md, docs/pilotage/PROJECT_STATUS.md, docs/pilotage/ROADMAP.md, docs/pilotage/CONTEXTE.md et docs/decisions/journal.md. Lire ensuite les documents métier indiqués par le ticket.
3. Vérifier la branche, le dernier commit et les modifications locales. Comparer à main sans écraser les travaux locaux. Les travaux de la PR #3 ne sont pas acquis dans main tant que non fusionnés.
4. Présenter un plan court, les fichiers concernés et les critères de validation avant modification.
## Règles
- Un ticket, une branche atomique, une PR ; pas de push direct sur main ni de force push. Fusion d'une PR uniquement après qualification applicable et autorisation humaine ; la coordination peut déléguer l'opération à son assistant. Revue indépendante pour les contributions de coordination. Ne pas clôturer un chantier métier incomplet.
- Collaboration IA active autorisée par le membre : créer/modifier les fichiers, exécuter les tests, créer une branche, committer, pousser et ouvrir une PR via son compte réellement authentifié, dans les limites des permissions. Aucun besoin de saisir manuellement chaque commande. Vérifier identité et attribution ; ne pas usurper un compte tiers ni masquer l'assistance IA. Le membre relit, comprend et valide son travail ; aucune preuve fabriquée ni contribution antidatée.
- Commits atomiques en français : titre, ticket, et corps détaillé pour les changements importants (objectif, méthode, tests, résultats, limites). PR en français avec preuves et relecteur humain distinct. Si l'accès réseau ou en écriture manque, utiliser un environnement autorisé (Codex, Claude Code ou Git local), sans contourner les permissions.
- Ne jamais demander ou committer de secrets, données personnelles non nécessaires ou fichiers sans licence vérifiée.
- Ne jamais inventer une donnée, un test, un accès ou une approbation. Distinguer vérifié, déclaré, hypothèse, non vérifié. Distinguer zéro et absence de données.
- Respecter les grains, dates de validité J+1/J+2, cohortes comparables, sources et limites ; pas de recommandation opérationnelle SDIS validée.
- Ne pas modifier les sections historiques des analyses individuelles ; documenter les compléments séparément.
- Exécuter les tests applicables, signaler ceux non exécutés et fournir commandes, résultats et liens.
## Fin de session
Rendre : ticket, branche, fichiers modifiés, tests et résultats, limites, prochaines actions, PR et revue requise. Proposer une mise à jour datée du statut et du journal si une décision ou un changement matériel intervient. Le ticket et GitHub vivant priment sur un instantané de statut obsolète. Voir CONTRIBUTING.md.
