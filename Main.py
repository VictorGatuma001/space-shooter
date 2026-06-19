#!/usr/bin/env python3
"""
Space Shooter
-------------
A Galaga-style shoot-em-up with multiple enemy types, power-ups, and a boss fight.

Run with: python3 main.py
"""

from game import Game


if __name__ == "__main__":
    game = Game()
    game.run()