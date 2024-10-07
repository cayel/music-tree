# Music Tree Project

## Description

Ce projet est une application Python qui utilise SQLite pour gérer une base de données musicale. Il permet de stocker des informations sur les artistes, les groupes et les albums, ainsi que leurs relations. Le projet utilise également NetworkX et Matplotlib pour visualiser les relations entre les entités sous forme de graphe.

## Fonctionnalités

- Création de la base de données SQLite avec les tables `Artist`, `Band`, `Album`, `BandArtist`, et `ArtistAlbum`.
- Ajout d'artistes, de groupes et d'albums dans la base de données.
- Gestion des relations entre les artistes et les groupes (`is member of`), ainsi qu'entre les artistes et les albums (`played`).
- Visualisation des relations sous forme de graphe avec des couleurs différentes pour chaque type de nœud et de relation.
