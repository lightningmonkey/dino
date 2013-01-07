from import_all import *
from animals import GenericAnimal

PLAYER_MAX_HEALTH = 300
PLAYER_SIZE = 1

class Player(GenericAnimal):
    """ The hero! Contains all the needed information about the player """
    def __init__(self, width, height, player_background, player_color ):
        super(Player, self).__init__(PLAYER_MAX_HEALTH, PLAYER_SIZE, width, height, player_background)
        self.player_color = player_color;
        assert( width == height ) #assume the player is a square for now
        self.dim = width
        self.create_player()
        
    def create_player(self):
        """ Draw the player """
        pygame.draw.circle(self.surface, self.player_color, (self.dim/2, self.dim/6), self.dim/6)
        pygame.draw.line(self.surface, self.player_color, (self.dim/2,self.dim/3), (self.dim/2,self.dim*(5.0/6.0)), 4)
        pygame.draw.line(self.surface, self.player_color, (self.dim/2,self.dim*(5.0/6.0)), (0,self.dim), 4)
        pygame.draw.line(self.surface, self.player_color, (self.dim/2,self.dim*(5.0/6.0)), (self.dim,self.dim), 4)
        pygame.draw.line(self.surface, self.player_color, (0,self.dim/2), (self.dim,self.dim/2), 4)