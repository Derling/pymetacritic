# pygamecritic
Python Api for retrieving critic and user scores from metacritic. Only meant to for viewing reviews for video game entries. 

## Usage
```python
import metagraphs as mg

metacritic = mg.MetaGraphs('the witcher 3 wild hunt') # main argument is the game name
```

### Secondary Module

```python
from metacritic import pygamecritic as pgn

metacritic = pgn.PyGameCritic('pc','xcom 2') # main arguments are the console and game.
metacritic.user_reviews # all user reviews 
metacritic.critic_reviews # all critic reviews 
print(metacritic) # formatted string representing the total number of reviews for a given game on a given console.
```
