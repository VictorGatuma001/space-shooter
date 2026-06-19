# Space Shooter

A retro-style Galaga-inspired space shooter built with Pygame. Fight through 6 waves of escalating enemies, collect power-ups, and face off against a final boss. Pure Python with procedurally-generated sprite graphics.

## Features

- **Multiple enemy types** — Drones (basic), Strikers (fast), Tanks (tanky), and a final Boss
- **Progressive difficulty** — 6 enemy waves that increase in challenge before the boss encounter
- **Dynamic power-ups** — Rapid Fire (faster shooting), Shield (damage negation), and Spread Shot (3-way bullets)
- **Retro pixel art** — All sprites generated procedurally using Pygame drawing, no external image files
- **Score-based progression** — Enemies are worth different points based on type and difficulty
- **Full game loop** — Menu, gameplay, game over, and win states

## Preview

```
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│                        Score: 2500                    Wave: 3  │
│                        HP: 3/3                                 │
│                                                                 │
│                           ◇ ◇                                  │
│                         ◇ ◇ ◇ ◇                               │
│                           ◇ ◇                                  │
│                                                                 │
│                    ■ ■           ■ ■                           │
│                  ■ ■ ■ ■       ■ ■ ■ ■                        │
│                    ■ ■           ■ ■                           │
│                                                                 │
│                        ○   ●   ○                               │
│                          ▲ △ ▲                                  │
│                                                                 │
│   RAPID FIRE                                                   │
│   SPREAD SHOT                                                  │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

`▲` is your ship. `■`/`◇`/`■` are different enemy types. `●` is your bullets. `○` are power-ups.

## Installation & Running

**Requirements:** Python 3.8+

```bash
git clone https://github.com/<your-username>/space-shooter.git
cd space-shooter
pip install -r requirements.txt
python3 main.py
```

## Controls

| Key | Action |
|---|---|
| `LEFT` / `A` | Move left |
| `RIGHT` / `D` | Move right |
| `SPACE` | Shoot |

Menu and game-over screens use `SPACE` to navigate.

## Game Progression

1. **Waves 1-2:** Basic drones to warm up
2. **Wave 3:** Strikers (faster enemies) join the mix
3. **Wave 4:** More drones with higher speed
4. **Wave 5:** Strikers return, tougher formation
5. **Wave 6:** Heavily armored Tanks that absorb multiple hits
6. **Boss:** A massive final enemy with 50 HP — one hit without a shield!

Each defeated enemy has a 15% chance to drop a random power-up.

## Project Structure

```
space_shooter/
├── main.py          # Entry point
├── game.py          # Main game loop and state management
├── entities.py      # Player, Enemy, Bullet, and PowerUp classes
├── sprites.py       # Procedural sprite generation
├── constants.py     # Game configuration
├── requirements.txt # Pygame dependency
└── .gitignore
```

**Architecture highlights:**
- **Separation of concerns** — Game logic, entity behavior, and rendering are independent
- **Sprite-based collisions** — Uses Pygame's built-in `pygame.sprite.spritecollide()` for clean hit detection
- **Procedural graphics** — No external asset files; all sprites are drawn procedurally at startup
- **Configurable waves** — Adding new enemy waves or tweaking difficulty is as simple as editing `WAVES` in `constants.py`

## Design Notes

- **Sprite generation:** Rather than including PNG files, all sprites are created on-the-fly using Pygame's drawing primitives (circles, polygons, rectangles). This keeps the project lightweight and makes visual tweaks easy.
- **Enemy AI:** Enemies follow a simple downward path with a gentle sine-wave motion for visual interest. Strikers move faster, Tanks move slower.
- **Power-up spawning:** When an enemy dies, there's a random chance it drops one of three power-up types. Power-ups are time-limited (5 seconds) to keep gameplay dynamic.
- **Collision system:** Uses Pygame's sprite groups and collision detection; clean and performant even with dozens of entities on screen.

## Possible Future Enhancements

- **Sound effects & music** — Add SFX for shooting, explosions, and background music
- **Particle effects** — Explosions, trails, and visual feedback for hits
- **Leaderboard** — Track high scores across sessions (using local file storage)
- **Difficulty modes** — Easy/Normal/Hard with different enemy patterns
- **More enemy types** — Shielded enemies, enemies that shoot back, etc.
- **Level progression** — Custom hand-designed wave patterns instead of just spawning randomly
- **Mobile support** — Touch controls for phones/tablets

## License

MIT — do whatever you'd like with it.
