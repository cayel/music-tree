# Music Tree Project

## Description

Ce projet est une application Python qui utilise SQLite pour gérer une base de données musicale. Il permet de stocker des informations sur les artistes, les groupes et les albums, ainsi que leurs relations. Le projet utilise également NetworkX et Matplotlib pour visualiser les relations entre les entités sous forme de graphe.

## Fonctionnalités

- Création de la base de données SQLite avec les tables `Artist`, `Band`, `Album`, `BandArtist`, et `ArtistAlbum`.
- Ajout d'artistes, de groupes et d'albums dans la base de données.
- Gestion des relations entre les artistes et les groupes (`is member of`), ainsi qu'entre les artistes et les albums (`played`).
- Visualisation des relations sous forme de graphe avec des couleurs différentes pour chaque type de nœud et de relation.

## Installation

1. Clonez le dépôt :
   ```sh
   git clone https://github.com/votre-utilisateur/music-tree.git
   cd music-tree

## Utilisation
- Exécutez le script pour créer la base de données et visualiser les relations :
  ```sh
    python app.py
- Le script va :
    - Créer la base de données SQLite et les tables nécessaires.
    - Ajouter des données d'exemple (artistes, groupes, albums).
    - Visualiser les relations sous forme de graphe.
      
## Modèle de données

```mermaid
erDiagram
    ARTIST {
        integer id
        string firstName
        string lastName
    }
    BAND {
        integr id
        string name
    }
    ALBUM {
        integer id
        string title
        date releaseDate
    }
    BAND only one to zero or more ALBUM : records
    ARTIST only one to zero or more BAND : "is member of"
    ARTIST only one to zero or more ALBUM : played
