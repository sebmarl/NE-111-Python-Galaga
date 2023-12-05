# This class handles sprite sheets
# This was taken from www.scriptefun.com/transcript-2-using
# sprite-sheets-and-drawing-the-background
# I've added some code to fail if the file wasn't found..
# Note: When calling images_at the rect is the format:
# (x, y, x + offset, y + offset)

# Additional notes
# - Further adaptations from https://www.pygame.org/wiki/Spritesheet
# - Cleaned up overall formatting.
# - Updated from Python 2 -> Python 3.

"""RG (Rohit G)"""
import pygame


class SpriteSheet:
    """ this class extracts individual sprite(images) from a single sprite-sheet for efficiency.
        1. calculating list of coord | 2. creating rectangular surfaces and blitzing sprite-sheet sections on it
        3. returning them as list of images  (RG)"""

    def __init__(self, filename):
        """Loads the sheet, converting image for fast per-pixel and transparency manipulation"""
        try:
            self.sheet = pygame.image.load(filename).convert_alpha()
            self.sheet.set_colorkey(-1, pygame.RLEACCEL)
            '''pixels with '-1' will be treated as transparent, to remove background (RG)'''

        except pygame.error as e:
            print(f"Unable to load spritesheet image: {filename}")
            raise SystemExit(e)
        ''' image error: prints message and exits program (RG)'''

    def image_at(self, rectangle, colorkey=None):
        """Load a specific image from a specific rectangle."""
        # Loads image from x, y, x+offset, y+offset.
        rect = pygame.Rect(rectangle)
        image = pygame.Surface(rect.size).convert()
        image.blit(self.sheet, (0, 0), rect)
        ''' assigns segment of spritesheet onto new surface (RG)'''
        if colorkey is not None:
            if colorkey == -1:
                colorkey = image.get_at((0, 0))
            image.set_colorkey(colorkey, pygame.RLEACCEL)
            ''' using colourkey parameter to handle transperancy (RG)'''
        return image

    def images_at(self, rects, colorkey=None):
        """Load a whole bunch of images and return them as a list."""
        return [self.image_at(rect, colorkey) for rect in rects]
        '''using for-loop with previous function returning an image list (RG)'''

    def load_strip(self, rect, image_count, colorkey=None):
        """Load a whole strip of images, and return them as a list."""
        tups = [(rect[0] + rect[2] * x, rect[1], rect[2], rect[3])
                for x in range(image_count)]
        return self.images_at(tups, colorkey)
        '''taking a single rectangle, calculates list of rectangles, incrementing by 'x' coord (RG)
         calls 'image_at' to load images from strip'''
