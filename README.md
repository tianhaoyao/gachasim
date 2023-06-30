# gachasim

A gacha game simulator. Define your own game/rarities/items and roll  
Users may add their own definition of a gacha game and share with their friends.

To run backend:  
`pip install -r requirements.txt`  
`python manage.py runserver`  

To run frontend:  
`cd frontend`  
`npm install`
`npm run serve`


## Backend
---
`GET /game/games/` - gets all games. Allows filtering/ordering by `id`  
`GET /game/rarities/` - gets all rarities. Allows filtering/ordering by `id`, `game_id`  
`GET /game/items/` - gets all items. Allows filtering/ordering by `id`, `rarity_id`  

`POST /game/games/` - add new game. Required fields `{"game_name": str, "image": image}`  
`POST /game/rarities/` - add new rarity associated with game `game_id`. Required fields `{"game_id": int(fk), "rarity_name": str, "chance": float, "color": HEX}`. Optional fields: `{"pity": int, "softpity": int, "softpitychance":float}`  
`POST /game/items/` - add new item associated with rarity `rarity_id`. Required fields `{"rarity_id": int(fk), "item_name": str, "image": image, "chance": float}`  

`GET /game/<game_id>/gacha/?numrolls=<numrolls>` - simulates rolling on the `<game_id>` game `numroll` times, returns an array of `rarity`, `item`, `pity`  

