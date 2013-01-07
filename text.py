from import_all import *

EATING = "NOM NOM"
TEXT_LIFE_CYLCE = 1000

class GenericText(GenericTimedSuface):
    def __init__(self, font, font_size, phrase, timer, color, x, y):
        super(GenericText, self).__init__(timer, 0, 0, TRANSPARENT, x, y)
        self.font = pygame.font.Font(font, font_size)
        self.surface = self.font.render(phrase, True, BLUE)
        self.textRect = self.surface.get_rect()
        self.textRect.center = (x, y)
        
class Eating(GenericText):
    def __init__(self, x, y):
        super(Eating, self).__init__('freesansbold.ttf', 30, EATING, TEXT_LIFE_CYLCE, BLUE, x, y)
        self.start_timer()