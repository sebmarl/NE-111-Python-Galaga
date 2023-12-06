"""AG(Advait Gore)"""

import sys
import pygame
#Class that runs the main game 
#This is the file that will run the game and the outputs, depending on what happens
from states.menu import Menu
from states.gameplay import Gameplay
from states.upgradeMenu import UpgradeMenu
from states.game_over import GameOver
from states.splash import Splash
from game import Game
import constants
import upgrades

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
    "UPGRADEMENU": UpgradeMenu(),
    "GAME_OVER": GameOver(),
}

game = Game(screen, states, "SPLASH")
game.run()
pygame.quit()
sys.exit()
