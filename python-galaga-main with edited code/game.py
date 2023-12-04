""" Sebastian Marion-Landais """ 
""" Rohit G."""
import pygame
import constants


class Game(object):
    def __init__(self, screen, states, start_state): 
        #initializes the game function and its states 
        self.done = False
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.fps = constants.FPS
        self.states = states
        self.state_name = start_state
        self.state = self.states[self.state_name] 

    def event_loop(self):
        #creates the gameplay loop 
        for event in pygame.event.get():
            self.state.get_event(event)

    def flip_state(self):
        # transition function to move from one state to another 
        next_state = self.state.next_state
        self.state.done = False
        self.state_name = next_state
        self.state = self.states[self.state_name]
        self.state.startup()

    def update(self, dt):
        #updates the flip state function 
        if self.state.quit:
            self.done = True
        elif self.state.done:
            self.flip_state()
        self.state.update(dt)

    def draw(self):
        #Draws the black background on the screen 
        self.screen.fill((0, 0, 0))
        self.state.draw(self.screen)

    def run(self):
        #Runs the game, while the method self.done is not met, it runs all the other methods necessary to run the game 
        while not self.done:
            dt = self.clock.tick(self.fps)
            self.event_loop()
            self.update(dt)
            self.draw()
            pygame.display.update()
