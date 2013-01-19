from import_all import *
from animals import GenericAnimal

PLAYER_MAX_HEALTH = 300
PLAYER_LEVEL = 0
PLAYER_LEVEL_LIST = [300, 5000, 10000]
PLAYER_ATTACK_MIN = 5
PLAYER_ATTACK_MAX = 8

class Player(GenericAnimal):
    """ The hero! Contains all the needed information about the player """
    def __init__(self):
        super(Player, self).__init__(PLAYER_MAX_HEALTH, PLAYER_LEVEL, PLAYER_LEVEL_LIST, PLAYER_ATTACK_MIN, PLAYER_ATTACK_MAX, PLAYER_DIMENSION_X, PLAYER_DIMENSION_Y, TRANSPARENT)
        self.player_color = RED;
        self.dim = PLAYER_DIMENSION_X
        self.create_player()
        logging.info('Created player||{0}'.format(self.__repr__()))
        
    def __repr__(self):
        s = super(Player, self).__repr__()
        return 'Player(player_color=%r)||%s' % (self.player_color, s)
        
    def __str__(self):
        s = super(Player, self).__str__()
        return 'Player-player_color:{0}||{1}'.format(self.player_color, s)
        
    def create_player(self):
        """ Draw the player """
        pygame.draw.circle(self.surface, self.player_color, (self.dim/2, self.dim/6), self.dim/6)
        pygame.draw.line(self.surface, self.player_color, (self.dim/2,self.dim/3), (self.dim/2,self.dim*(5.0/6.0)), 4)
        pygame.draw.line(self.surface, self.player_color, (self.dim/2,self.dim*(5.0/6.0)), (0,self.dim), 4)
        pygame.draw.line(self.surface, self.player_color, (self.dim/2,self.dim*(5.0/6.0)), (self.dim,self.dim), 4)
        pygame.draw.line(self.surface, self.player_color, (0,self.dim/2), (self.dim,self.dim/2), 4)
    
    def level_up(self):
        print('Player leveled up!')