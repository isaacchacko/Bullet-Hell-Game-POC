# Bullet Hell Game (Proof of Concept)

This is a simple game built off of the pygame library (ver. 2.0.0) that follows the bullet hell genre.

Controls are WASD.

Control of the player is pretty hard to get used to (from what I've heard, feels fine myself :D).

Quirks:

- Game will enter "bullet time" if a bullet becomes too close to the player (range of 100 pixels). 
- doesn't accurately show collision at time of death. Game grays out before collision one frame before actual collision, as the collision is calculated before displaying objects on screen.
- No button to restart the game, must be restarted by re-running the program.
- Fonts used in game are from the font files in the repository.



If you ever want to change/mutate any part of the game (i.e. the bullet speed, the player movement, etc.), the code is mostly readable to a layman.