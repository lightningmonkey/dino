from import_all import *
from animals import GenericAnimal

PLAYER_MAX_HEALTH = 300
PLAYER_LEVEL = 0
PLAYER_LEVEL_LIST = [300, 5000, 10000]

class Player(GenericAnimal):
    """ The hero! Contains all the needed information about the player """
    def __init__(self, width, height, player_background, player_color ):
        super(Player, self).__init__(PLAYER_MAX_HEALTH, PLAYER_LEVEL, PLAYER_LEVEL_LIST, width, height, player_background)
        self.player_color = player_color;
        assert( width == height ) #assume the player is a square for now
        self.dim = width
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