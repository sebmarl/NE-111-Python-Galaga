""" SM (Sebastian Marion-Landais) """
import pygame


class Explosion(pygame.sprite.Sprite):
    def __init__(self, sprites, x, y):
        super(Explosion, self).__init__()
        self.timer = 0
        self.interval = 2
        self.number_of_images = 10
        self.images = sprites.load_strip([64, 0, 64, 64], 3, -1)
        self.images.extend(sprites.load_strip([0, 64, 64, 64], 4, -1))
        self.images.extend(sprites.load_strip([0, 128, 64, 64], 3, -1))

        for index, image in enumerate(self.images):
            self.images[index] = pygame.transform.scale(image, (128, 128))

        self.surf = self.images[0]
        self.rect = self.surf.get_rect(center=(x, y))
        self.image_index = 0

    def get_event(self, event):
        pass

    def update(self, pressed_keys):
        self.timer += 1
        if self.timer % self.interval == 0:
            self.image_index += 1

        if self.image_index >= self.number_of_images:
            self.kill()

    def get_surf(self):
        return self.images[self.image_index]
#Explosion class, subclass of pygame.sprite.Sprite. Similar to the enemy and player class,\ 
#the init method is called to initialize the appearance,position and size of the explosion.\
#like the previous update functions as well, this update function updates the objects appearance\
 #and timer. It loads the images using the load_strip method, these images are then stored into the\
 #self.images list. The get_surf function gets the surface in order to display the explosion on the screen. SM """ 
