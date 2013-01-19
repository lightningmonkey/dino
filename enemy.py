from import_all import *
from animals import GenericAnimal

class Compsognathus(GenericAnimal):
    """ Small meat eating dino """
    def __init__(self, x, y):
        super(Compsognathus, self).__init__(50, 0, [0], 1, 5, 30, 30, TRANSPARENT)
        self.enemy_color = ORANGE;
        self.dim = self.surface_width
        self.x = x
        self.y = y
        self.create_enemy()
        logging.info('Created player||{0}'.format(self.__repr__()))
        
    def __repr__(self):
        s = super(Compsognathus, self).__repr__()
        return 'Compsognathus(enemy_color=%r)||%s' % (self.enemy_color, s)
        
    def __str__(self):
        s = super(Compsognathus, self).__str__()
        return 'Compsognathus-enemy_color:{0}||{1}'.format(self.enemy_color, s)
        
    def create_enemy(self):
        """ Draw the enemy """
        pygame.draw.circle(self.surface, self.enemy_color, (self.dim/2, self.dim/6), self.dim/6)
        pygame.draw.line(self.surface, self.enemy_color, (self.dim/2,self.dim/3), (self.dim/2,self.dim*(5.0/6.0)), 4)
        pygame.draw.line(self.surface, self.enemy_color, (self.dim/2,self.dim*(5.0/6.0)), (0,self.dim), 4)
        pygame.draw.line(self.surface, self.enemy_color, (self.dim/2,self.dim*(5.0/6.0)), (self.dim,self.dim), 4)
        pygame.draw.line(self.surface, self.enemy_color, (0,self.dim/2), (self.dim,self.dim/2), 4)