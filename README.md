# 🚀 Shoot Them Up

**"Shoot Them Up"** is a side-scrolling arcade-style space shooter built using Python and Pygame. You play as a lone space pilot defending Earth from a storm of asteroids and alien enemies. Collect power-ups, dodge enemy bullets, and see how long you can survive!

---

## 🎮 Features

* **Player Controls**
  Move with arrow keys and shoot with the space bar.

* **Enemies & Rocks**
  Randomly moving enemies and rotating asteroids with varying damage and scores.

* **Power-Ups**

  * **Shield**: Restores your shield (up to 100%).
  * **Bolt**: Enhances your shooting power temporarily.

* **Explosions**
  Animated explosions for player, enemies, and objects.

* **Sound Effects & Music**
  Background music and FX like laser blasts and explosions.

---

## 🕹️ Gameplay Rules

* **Lives**: Start with 3 lives. When your shield hits 0, you lose one life.
* **Game Over**: The game ends when all lives are lost.
* **Power-Up Timer**: Bolt power-up lasts 5 seconds.
* **Scoring**:

  * Rocks: Varying points based on size.
  * Enemies: Fixed score per enemy type.

---

## 📁 Project Structure

```
ShootThemUp/
├── image/
│   ├── playerShip1_orange.png
│   ├── background.jpg
│   ├── enemies/
│   ├── rock/
│   ├── explosion/
│   └── powerups/
├── sound/
│   ├── background.mp3
│   ├── explosion.wav
│   └── laser.ogg
├── main.py
└── README.md
```

---

## 🛠️ Setup Instructions

### Prerequisites

* Python 3.x
* Pygame

### Installation

```bash
pip install pygame
```

### Run the Game

```bash
python main.py
```

---

## 🚧 Known Bugs / To-Do

* Occasionally enemy bullets pass through the player without collision.
* Add more enemy types and attack patterns.
* Implement high score tracking.

---


## 💡 Credits

* Built with ❤️ using [Pygame](https://www.pygame.org/news)
* Art and sound from royalty-free online assets (OpenGameArt, Kenney Assets, etc.)

---

## 📜 License

This project is open-source and free to use under the MIT License.


