SM (Sebastian Marion-Landais) 
from bezier.control_point_handler import ControlPointHandler
import pygame


class ControlPoint(pygame.sprite.Sprite):
    def __init__(self, x, y, color, q_index,
                 p_index, control_points,
                 control_handler_mover: ControlPointHandler):
        super(ControlPoint, self).__init__()

        self.control_points = control_points
        self.q_index = q_index
        self.p_index = p_index
        self.control_handler_mover = control_handler_mover
        self.original_image = pygame.Surface((50, 50), pygame.SRCALPHA)
        pygame.draw.circle(self.original_image, color, (25, 25), 10)
        self.selected_image = pygame.Surface((50, 50), pygame.SRCALPHA)
        pygame.draw.circle(self.selected_image, color, (25, 25), 10)
        pygame.draw.circle(self.selected_image, (255, 255, 255), (25, 25), 10, 2)
        self.image = self.original_image
        self.rect = self.image.get_rect(center=(x, y))
        self.selected = False
"""The code above is for creating a control point class. This class comes from pygame.sprite.Sprite\
it can be used with sprite groups and is controlled by the pygame sprite group methods. There are\
multiple different attributes the class uses. It is used to control the bezier curve that  Patrick Kalkman\
used as the movement path for the insectoids SM """ 

    def get_event(self, event):
        pass

    def update(self, keys):
        mouse_pos = pygame.mouse.get_pos()
        mouse_buttons = pygame.mouse.get_pressed()
        self.selected = self.rect.collidepoint(
            mouse_pos) and any(mouse_buttons)
        self.image = self.selected_image if self.selected else self.original_image

        if self.selected:
            self.rect = self.image.get_rect(
                center=(mouse_pos[0], mouse_pos[1]))
            self.control_handler_mover.move_control_handler(
                ControlPointHandler(self.q_index, self.p_index),
                mouse_pos[0], mouse_pos[1])
        else:
            self.x = self.control_points.get_quartet(
                self.q_index).get_point(self.p_index).x
            self.y = self.control_points.get_quartet(
                self.q_index).get_point(self.p_index).y
            self.rect = self.image.get_rect(center=(self.x, self.y))
""" Controls the points position, appearance and selected state. The function is the update method\
for the ControlPoint class and function created above. It checks the mouse position, which button was pressed\
Then it checks if the mouse cursor is over the control point, then if the cursor was over the \
control point the image attribut gets set to selected image, otherwise it goes to original image.\ 
Then if the control point is selected, the positions of the control point are updated.  SM """ 

    def get_surf(self):
        return self.image
