""" SM (Sebastian Marion-Landais) """ 
"""Advait Gore"""

import math
import pygame
import constants

from bezier.path_point_calculator import \
    PathPointCalculator


class Enemy(pygame.sprite.Sprite):
    def __init__(self, sprites, control_points, enemy):
        super(Enemy, self).__init__()
        self.rotation = 0
        self.timer = 0
        self.control_points = control_points
        self.bezier_timer = 0.0
        self.interval = 2
        self.sprite_index_count = 0
        #Changed the sprite_index_count from 1 to zero in order to get the images to stop rotation SM 

        if enemy == 0:
            self.number_of_images = 5
            self.images = sprites.load_strip([10,366,63,75], self.number_of_images, 0)
        elif enemy == 1:
            self.number_of_images = 5
            self.images = sprites.load_strip([10,366,63,75], self.number_of_images, 0)
        elif enemy == 2:
            self.number_of_images = 5
            self.images = sprites.load_strip([10,366,63,75], self.number_of_images, 0)

        self.surf = self.images[0]
        self.rect = self.surf.get_rect(center=(constants.SCREEN_WIDTH / 2, constants.SCREEN_HEIGHT - 20))
        self.image_index = 0
        self.calculator = PathPointCalculator()
        self.previous_point = None
        self.rotation_calc = 0
        #Defines the enemy class. The enemy class is a subclass of pygame.sprite.Sprite. Follows\
#the bezier curve path along its control points. The init function keeps track of the enemy's\
#position, rotation and appearance.  

    def get_event(self, event):
        pass

    def update(self, keys):
        control_point_index = int(self.bezier_timer)
        path_point = self.calculator.calculate_path_point(
            self.control_points.get_quartet(control_point_index), self.bezier_timer)
        if self.previous_point is None:
            self.previous_point = path_point

        self.rotation = self.calculate_rotation(self.previous_point, path_point)
        self.previous_point = path_point
        self.rect.centerx = path_point.xpos
        self.rect.centery = path_point.ypos
        self.timer += 1
        self.bezier_timer += 0.012
        if int(self.bezier_timer) > self.control_points.number_of_quartets() - 1:
            self.kill()
            #Updates enemy position and appearance. uses the PathPointCalculator in order to do this  

    def calculate_rotation(self, previous_point, current_point):
        dx = current_point.xpos - previous_point.xpos
        dy = current_point.ypos - previous_point.ypos

        return 180 * math.degrees(math.atan2(dx, dy))
        # calculates the next path point for the object "the enemy insectoids"  

    def get_surf(self):
        if self.timer % self.interval == 0:
            self.image_index += self.sprite_index_count
            if self.image_index == self.number_of_images - 1 or \
                    self.image_index == 0:
                self.sprite_index_count = -self.sprite_index_count

        rot_image = pygame.transform.rotate(self.images[self.image_index], self.rotation)
        self.rect = rot_image.get_rect(center=self.rect.center)
        #The get_surf function gets the surface of the enemy in order to display it on the screen. This is important to the\
#update function in order to render the enemy on the screen. SM 

        return rot_image
