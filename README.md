# Space War Pygame
Pygame project, a game called space war. The game contains background music and different sound and visual effects. This 2D game is the best situs for people who has a range of 4+. 

## Rules Instructions
1. Press any key to start the game
2. Press the space key to shoot
3. Use left and right arrow keys to move horizontally

### Additional information
1. You have a total of 3 lives
2. The bolt powerups will allow you to have two slits of laser
3. The shield powerups will allow you to recover
4. The rocks of different sizes have different damage when hits the spaceship you are controlling, try to destroy them before you get damaged.
5. Your enemies can also fire lasers at you, they can move in different directions, try to destroy your enemies spaceships otherwise they will damage you.
6. Destroying rocks and enemies will both increase your score, your score is recorded on the top of the screen.

# Damage, scores and powerups table
1. Player shield/health = 100 per life, players have a total of 3 lives
2. When enemy bullet(laser) hits player, player shield/health - 45
3. When player hits small rocks(shield/health - 10), mid rocks(shield/health - 30), large rocks(shield/health - 50), largest rock(shield/health - 70)
4. When a player hits enemy, shield/health - 95
5. When player destroy small rocks(score + 10), mid rocks(score + 8), large rocks(score + 4), largest rock(score + 1)
6. When players destroy enemies spaceships, score + 5
7. When the player hits shield powerups, player shield/health + 30
8. When the player hits bolt powerups, laser level up, from one slit to two slits

# Environment
Developed in python 3.7 - pygame, using PyCharm.
