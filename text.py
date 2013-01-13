from import_all import *

EATING = "NOM NOM"
TEXT_LIFE_CYLCE = 1000

class GenericText(GenericTimedSurface):
    """ A surface to write things on """
    def __init__(self, font, font_size, phrase, timer, color, x, y, parent = None):
        super(GenericText, self).__init__(timer, 0, 0, TRANSPARENT, x, y)
        self.font = pygame.font.Font(font, font_size)
        self.surface = self.font.render(phrase, True, BLUE) #Font creates a surface, get the data from that surface
        self.surface_width = self.surface.get_width()
        self.surface_height = self.surface.get_height()
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
    def __init__(self, parent):
        super(Eating, self).__init__('freesansbold.ttf', 20, EATING, TEXT_LIFE_CYLCE, BLUE, 0, 0, parent)
        #want to always have the text in the center of the parent
        center_x = parent.surface_width/2 + parent.x
        center_y = parent.surface_height/2 + parent.y
        self.x = center_x - self.surface_width/2
        self.y = center_y - self.surface_height/2
        self.start_timer()