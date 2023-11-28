from .tools import time_millis
import pygame
from . import constants as c, tools
from .constants import Rectangle
from .tools import grab_sheet 
from bezier.path_point_calculator import \
    PathPointCalculator


class GalagaSprite(pygame.sprite.Sprite):
    """
    Base class for a general sprite in Galaga.
    Useful for sprites that can flip their images, show/hide, and have their images offset from
    their centers, as well as having centered sprites.
    """

    def __init__(self, x, y, width, height, *groups: pygame.sprite.Group):
        super(GalagaSprite, self).__init__(groups)

        # Rectangle and position
        self.rect = pygame.Rect(0, 0, width, height)
        self.x = x
        self.y = y

        # Display and image variables
        self.image = None
        self.image_offset_x: int = 0
        self.image_offset_y: int = 0
        self.is_visible: bool = True
        self.flip_horizontal: bool = False
        self.flip_vertical: bool = False


    @property
    def x(self):
        return self.rect.centerx

    @x.setter
    def x(self, value: int):
        self.rect.centerx = value

    @property
    def y(self):
        return self.rect.centery

    @y.setter
    def y(self, value: int):
        self.rect.centery = value

    def update(self, delta_time: int, flash_flag: bool):
        pass

    def display(self, surface: pygame.Surface):
        if self.image is not None and self.is_visible:
            image = pygame.transform.flip(self.image, self.flip_horizontal, self.flip_vertical)
            img_width, img_height = image.get_size()
            # Center the image
            x = self.x - img_width // 2 + self.image_offset_x
            y = self.y - img_height // 2 + self.image_offset_y
            surface.blit(image, (x, y))


class Player(GalagaSprite):

    def __init__(self, x, y):
        super(Player, self).__init__(x, y, 14, 12)
        self.image = grab_sheet(6 * 16, 0 * 16, 16, 16)
        self.image_offset_x = 1

    def update(self, delta_time, keys):
        s = round(c.PLAYER_SPEED * delta_time)
        if keys[pygame.K_RIGHT]:
            self.x += s
        elif keys[pygame.K_LEFT]:
            self.x -= s


class Enemy(pygame.sprite.Sprite):
    def __init__(self, sprites, control_points, enemy):
        super(Enemy, self).__init__()
        self.rotation = 0
        self.timer = 0
        self.control_points = control_points
        self.bezier_timer = 0.0
        self.interval = 2
        self.sprite_index_count = 1

        if enemy == 0:
            self.number_of_images = 7
            self.images = sprites.load_strip([0, 199, 48, 40], self.number_of_images, -1)
        elif enemy == 1:
            self.number_of_images = 4
            self.images = sprites.load_strip([0, 248, 48, 40], self.number_of_images, -1)
        elif enemy == 2:
            self.number_of_images = 4
            self.images = sprites.load_strip([0, 62, 64, 66], self.number_of_images, -1)

        self.surf = self.images[0]
        self.rect = self.surf.get_rect(center=(constants.SCREEN_WIDTH / 2, constants.SCREEN_HEIGHT - 20))
        self.image_index = 0
        self.calculator = PathPointCalculator()
        self.previous_point = None
        self.rotation_calc = 0

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

    def calculate_rotation(self, previous_point, current_point):
        dx = current_point.xpos - previous_point.xpos
        dy = current_point.ypos - previous_point.ypos

        return math.degrees(math.atan2(dx, dy)) + 180

    def get_surf(self):
        if self.timer % self.interval == 0:
            self.image_index += self.sprite_index_count
            if self.image_index == self.number_of_images - 1 or \
                    self.image_index == 0:
                self.sprite_index_count = -self.sprite_index_count

        rot_image = pygame.transform.rotate(self.images[self.image_index], self.rotation)
        self.rect = rot_image.get_rect(center=self.rect.center)

        return rot_image
        
     
    


class Missile(GalagaSprite):
    ENEMY_MISSILE = 246, 51, 3, 8
    PLAYER_MISSILE = 246, 67, 3, 8

    def __init__(self, x, y, vel, is_enemy):
        super(Missile, self).__init__(x, y, 2, 10)
        self.vel = vel
        self.is_enemy = is_enemy

        if self.is_enemy:
            img_slice = self.ENEMY_MISSILE
        else:
            img_slice = self.PLAYER_MISSILE
        ix, iy, w, h = img_slice
        self.image = grab_sheet(ix, iy, w, h)

    def update(self, delta_time: int, flash_flag: bool):
        vel = self.vel * delta_time
        self.x += round(vel.x)
        self.y += round(vel.y)


class Explosion(GalagaSprite):
    PLAYER_FRAME_DURATION = 140
    OTHER_FRAME_DURATION = 120

    PLAYER_FRAMES = [Rectangle(64, 112, 32, 32), Rectangle(96, 112, 32, 32), Rectangle(128, 112, 32, 32),
                     Rectangle(160, 112, 32, 32)]

    OTHER_FRAMES = [Rectangle(224, 80, 16, 16), Rectangle(240, 80, 16, 16), Rectangle(224, 96, 16, 16),
                    Rectangle(0, 112, 32, 32), Rectangle(32, 112, 32, 32)]

    def __init__(self, x: int, y: int, is_player_type=False):
        super(Explosion, self).__init__(x, y, 16, 16)
        self.is_player_type = is_player_type

        self.frame_timer = 0

        if self.is_player_type:
            self.image = grab_sheet(64, 112, 32, 32)
            self.frames = iter(self.PLAYER_FRAMES)
            self.frame_duration = self.PLAYER_FRAME_DURATION
        else:
            self.image = grab_sheet
            self.frames = iter(self.OTHER_FRAMES)
            self.frame_duration = self.OTHER_FRAME_DURATION

        self.frame = None
        self.next_frame()

    def next_frame(self):
        self.frame = next(self.frames)
        x, y, w, h = self.frame
        self.image = grab_sheet(x, y, w, h)
        self.frame_timer = 0

    def update(self, delta_time: int, flash_flag: bool):
        self.frame_timer += delta_time
        if self.frame_timer >= self.frame_duration:
            try:
                self.next_frame()
            except StopIteration:
                self.kill()
                return

    def display(self, surface: pygame.Surface):
        super(Explosion, self).display(surface)


def create_score_surface(number):
    sheet_y = 240
    char_width = 5
    char_height = 8
    sheet_char_width = 4

    number = int(number)
    str_num = str(number)
    length = len(str_num)

    # Create the surface to add to
    # noinspection PyArgumentList
    surface = pygame.Surface((char_width * length, char_height)).convert_alpha()

    # choose color based on the number
    color = None
    if number in (800, 1000):
        color = c.BLUE
    else:
        color = c.YELLOW

    # blit each individual char
    for i, character in enumerate(str_num):
        value = int(character)
        sheet_x = value * sheet_char_width
        number_sprite = grab_sheet(sheet_x, sheet_y, 4, 8)
        surface.blit(number_sprite, (i * char_width, 0))

    # replace white with color
    pixels = pygame.PixelArray(surface)
    pixels.replace((255, 255, 255), color)
    pixels.close()

    return surface


class ScoreText(GalagaSprite):
    # The class keeps track of the text sprites
    text_sprites = pygame.sprite.Group()

    def __init__(self, x, y, number, lifetime=950):
        super(ScoreText, self).__init__(x, y, 1, 1, self.text_sprites)  # BB size doesn't matter here
        self.number = number
        self.image = create_score_surface(self.number)
        self.lifetime = lifetime

    def update(self, delta_time: int, flash_flag: bool):
        # Wait to die
        if self.lifetime < 0:
            self.kill()
            return
        self.lifetime -= delta_time
