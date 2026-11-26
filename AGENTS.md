# Instructions pour tout assistant IA
Projet pédagogique HETIC MD5, SDIS 31 fictif, Occitanie. Langue de travail : français.
## Avant toute tâche
1. Identifier le ticket GitHub et son responsable réel ; lire son corps, commentaires, dépendances et PR liées. Si accès indisponible, demander les extraits nécessaires.
2. Lire README.md, docs/pilotage/PROJECT_STATUS.md, docs/pilotage/ROADMAP.md, docs/pilotage/CONTEXTE.md et docs/decisions/journal.md. Lire ensuite les documents métier indiqués par le ticket.
3. Vérifier la branche, le dernier commit et les modifications locales. Comparer à main sans écraser les travaux locaux. Les travaux de la PR #3 ne sont pas acquis dans main tant que non fusionnés.
4. Présenter un plan court, les fichiers concernés et les critères de validation avant modification.
## Règles
- Un ticket, une branche atomique, une PR ; pas de push direct sur main, de force push, de merge ni de clôture sans validation humaine.
- Ne pas produire de commits au nom d'autrui, fabriquer des preuves ou antidater une contribution. Chaque membre doit comprendre et vérifier son travail.
- Ne jamais demander ou committer de secrets, données personnelles non nécessaires ou fichiers sans licence vérifiée.
- Ne jamais inventer une donnée, un test, un accès ou une approbation. Distinguer vérifié, déclaré, hypothèse, non vérifié. Distinguer zéro et absence de données.
- Respecter les grains, dates de validité J+1/J+2, cohortes comparables, sources et limites ; pas de recommandation opérationnelle SDIS validée.
- Ne pas modifier les sections historiques des analyses individuelles ; documenter les compléments séparément.
- Exécuter les tests applicables, signaler ceux non exécutés et fournir commandes, résultats et liens.
## Fin de session
Rendre : ticket, branche, fichiers modifiés, tests et résultats, limites, prochaines actions, PR et revue requise. Proposer une mise à jour datée du statut et du journal si une décision ou un changement matériel intervient. Le ticket et GitHub vivant priment sur un instantané de statut obsolète. Voir CONTRIBUTING.md.
