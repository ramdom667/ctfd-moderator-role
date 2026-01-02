# CTFd Moderator Role Plugin

## 🎓 Cadre de Réalisation
Ce projet a été développé dans le cadre d'un projet universitaire en **BUT Informatique (IUT)**. La réalisation a suivi la méthodologie **Agile Scrum**, impliquant des cycles de développement itératifs et des échanges constants avec un client pour répondre à des besoins précis de gestion d'équipe.

## 📝 Description
`ctfd-moderator-role` est une extension Flask pour CTFd permettant de définir un rôle de modérateur intermédiaire. Il permet à des utilisateurs désignés d'accéder au panel d'administration pour gérer les flags tout en leur interdisant l'accès aux configurations sensibles du système.

## ✨ Fonctionnalités
- **Sécurisation des Routes (Backend)** : Blocage automatique de l'accès aux routes critiques (`/admin/config`, `/admin/pages`, `/admin/scoreboard`) pour les utilisateurs modérateurs via des interceptions de requêtes Flask.
- **Nettoyage Dynamique de l'UI (Frontend)** : Injection de scripts JavaScript pour masquer les éléments de menu interdits et les boutons de modification de défis (comme "New Challenge") afin de simplifier l'expérience utilisateur.
- **Configuration Flexible** : Liste de modérateurs basée sur les IDs utilisateurs définis dans le code source.

## 🛠️ Installation
1. Cloner le dépôt dans le dossier `CTFd/plugins/`.
2. Configurer les IDs des modérateurs dans `MODERATOR_IDS` au sein du fichier `__init__.py`.