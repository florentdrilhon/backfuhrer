# BackFührer

Gestion backend et base de données pour l'application PartyFührer du **BDE Nova** 🌌


## Services et pré-requis 🛠

Le backend se divise en plusieurs partie

- Base de données: MongoDB disponible aux identifiants pôle [ici](https://cloud.mongodb.com/v2/60b7af0739820a4aff0d3378#clusters) 
- Gestion de la base avec du Python
- API RESTful: Flask, disponible [ici](https://backfuhrer-api.herokuapp.com/)
- Interface admin: Flask, disponible avec les identifiants dans le *config.json* [ici](https://backfuhrer-api.herokuapp.com/admin) 


Pour plus de détails, la base de données est une base MongoDB Atlas (DB cloud, version gratos) et peut accueillir 500mo.

Le code python intéragit avec la base à l'aide du module *pymongo*, et a ensuite son propre schema de données défini pour manipuler les différentes entités dans le code.

Les données sont ensuite rendues disponible via l'API flask.


## Schema de données 📂

##### Description des differentes tables de données en base de données et leurs attributs.

Les différents modèles peuvent être retrouvés dans le module *core/models*

Chaque entité d'un modèle possède des attributs *_id* , *created_at* et *updated_at* pour les différencier et tracer leur existence 


### Jeux 


Les jeux font références aux jeux de type jeu d'alcool et je de soirées.

##### Attributs: 

- **name**, texte: Nom du jeu
- **description**, texte: description du jeu
- **rules**, texte: les règles du jeu
- **duration_min**, entier: durée du jeu en minutes
- **number_of_players**, tuple d'entiers: nombre de joueurs min et max
- **game_type**, custom text: type du jeu, il existe trois types pour l'instant : *cards*, *dice* et *other*











