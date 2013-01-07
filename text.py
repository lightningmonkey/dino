from import_all import *

EATING = "NOM NOM"
TEXT_LIFE_CYLCE = 1000

class GenericText(GenericTimedSuface):
    """ A surface to write things on """
    def __init__(self, font, font_size, phrase, timer, color, x, y, parent = None):
        super(GenericText, self).__init__(timer, 0, 0, TRANSPARENT, x, y)
        self.font = pygame.font.Font(font, font_size)
        self.surface = self.font.render(phrase, True, BLUE)
        self.set_parent(parent)
        
    def set_parent(self, parent):
        """ We need to know the parent so we know who to redraw then the text disappears"""
        assert(isinstance(parent, GenericSurface) or None == parent) #The parent needs to be a surface or this is no point
        self.parent = parent
        
    def get_parent(self):
        """ Return the parent """
        return self.parent
    
class Eating(GenericText):
    """ When you eat a tree """
    def __init__(self, x, y, parent = None):
        super(Eating, self).__init__('freesansbold.ttf', 20, EATING, TEXT_LIFE_CYLCE, BLUE, x, y, parent)
        self.start_timer()