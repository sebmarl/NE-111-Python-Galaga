"""AG(Advait Gore) and RG (Rohit G)"""
import sys
import pygame
# Class that runs the main game
# This is the file that will run the game and the outputs, depending on what happens
from states.menu import Menu
from states.gameplay import Gameplay
from states.game_over import GameOver
from states.splash import Splash
from game import Game
import constants

# setup mixer to avoid sound lag
pygame.mixer.pre_init(44100, -16, 2, 2048)
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((constants.SCREEN_WIDTH,
                                  constants.SCREEN_HEIGHT))
states = {
    "MENU": Menu(),
    "SPLASH": Splash(),
    "GAMEPLAY": Gameplay(),
    "GAME_OVER": GameOver(),  # collection of key for game states class (RG)
}

game = Game(screen, states, "SPLASH")  # creates game class, parameters: pygame screen, game states and init state"
game.run()
pygame.quit()
sys.exit()  # game loop init and exit (RG)
