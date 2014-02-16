from import_all import *
from sets import Set
from player import Player
from background import Background
from scenery import GenericScenery, SceneryTests
from animals import AnimalsTests, GenericAnimal
from text import Eating, GenericText
# from map import Map, MapTests


class MainLoop(object):
    """ The main event loop for the game"""

    def __init__(self, file_name):
        pygame.init()
        self.display_surf = pygame.display.set_mode((WINDOW_SIZE_X, WINDOW_SIZE_Y), 0, 32)
        pygame.display.set_caption("Dinosaurs Evolved")

        self.change = False  # Used to see if the board needs to be redrawn
        self.down_keys = Set()  # The keys that the user is currently holding down
        self.player = Player()
        self.background = Background(file_name)
        self.loop()

    def change_movement(self, event):
        """ When a key is pushed down or let up, change the down_keys list """
        if event.type == KEYDOWN:
            self.down_keys.add(event.key)
        elif event.type == KEYUP:
            self.down_keys.remove(event.key)

    def bounds_check(self, x, y):
        """ Make sure the player can no leave the playable surface """
        background_rect = pygame.Rect(x + OFFSET_X, y + OFFSET_Y, self.background.map.PLAYABLE_DIMENSION_X,
                                      self.background.map.PLAYABLE_DIMENSION_Y)
        player_rect = pygame.Rect(WINDOW_SIZE_X / 2, WINDOW_SIZE_Y / 2, PLAYER_DIMENSION_X, PLAYER_DIMENSION_Y)
        return background_rect.contains(player_rect)

    def object_check(self, x, y):
        """ Make sure the player can not run over any object on the map """
        player_rect = pygame.Rect(x, y, PLAYER_DIMENSION_X, PLAYER_DIMENSION_Y)
        for current_object in self.background.all_objects:
            object_rect = pygame.Rect(current_object.x, current_object.y, current_object.surface_width,
                                      current_object.surface_height)
            if player_rect.colliderect(object_rect):
                if isinstance(current_object, GenericScenery):
                    food_qty = current_object.get_food()
                    if food_qty > 0:
                        print("NOM  NOM")
                        self.player.eat_food(food_qty)
                        text = Eating(current_object)
                        logging.info("Added text: {0}".format(str(text)))
                        self.background.add_object(text)
                        self.change = True
                if isinstance(current_object, GenericAnimal):
                    player_attack = self.player.attack()
                    enemy_attack = current_object.attack()
                    player_dead = self.player.take_damage(enemy_attack)
                    enemy_dead = current_object.take_damage(player_attack)
                    print 'Player {0} {1} enemy {2} {3}'.format(self.player.get_health(), player_dead,
                                                                current_object.get_health(), enemy_dead)
                    logging.info(
                        'Attack! Player {0} alive {1} enemy {2} alive {3}'.format(self.player.get_health(), player_dead,
                                                                                  current_object.get_health(),
                                                                                  enemy_dead))
                    if not enemy_dead:
                        logging.info('Enemy killed: {0}'.format(str(current_object)))
                        self.background.all_objects.remove(current_object)
                        self.background.draw_all()
                return False
        return True

    def move_check(self, x, y):
        """ Given the x,y that the player wants to move to make sure nothing is in the way """
        return self.bounds_check(x, y) and self.object_check(-x, -y)

    def move(self):
        """Move the background, not the player. 
        
        As the player moves around, we also want to make sure they are centered in the screen. This means
        that it is the background that needs to move while the player stays stationary. Thus all the movements
        are 'backwards' below.  The the player wants to move to the right, move the board to the left. 
        
        """
        for k in self.down_keys:
            if k == K_DOWN or k == K_s:
                tmpy = self.background.y - STEP_SIZE
                if self.move_check(self.background.x, tmpy):
                    self.background.y = tmpy
            elif k == K_UP or k == K_w:
                tmpy = self.background.y + STEP_SIZE
                if self.move_check(self.background.x, tmpy):
                    self.background.y = tmpy
            elif k == K_RIGHT or k == K_d:
                tmpx = self.background.x - STEP_SIZE
                if self.move_check(tmpx, self.background.y):
                    self.background.x = tmpx
            elif k == K_LEFT or k == K_a:
                tmpx = self.background.x + STEP_SIZE
                if self.move_check(tmpx, self.background.y):
                    self.background.x = tmpx
            self.player.x = -self.background.x  # Since we start at (0.0) this will always be true
            self.player.y = -self.background.y

    def redraw(self):
        """ Update the display """
        if self.change:
            self.background.redraw()
            self.change = False
        self.display_surf.blit(self.background.get_surface(), (self.background.x, self.background.y))
        self.display_surf.blit(self.player.get_surface(), (WINDOW_SIZE_X / 2, WINDOW_SIZE_Y / 2))
        pygame.display.update()

    def update_objects(self):
        for current_object in self.background.all_objects:
            if isinstance(current_object, GenericTimedSurface):
                if isinstance(current_object, GenericScenery):
                    self.change = self.change or current_object.food_respawn()
                elif isinstance(current_object, GenericText):
                    if current_object.timer_fire():
                        current_object.get_parent().set_change()
                        self.background.all_objects.remove(current_object)
                        self.change = True

    def loop(self):
        """ The main loop that drives the game"""
        assert (0 == self.player.x)  # if the player does not start at (0,0) the later positions are all screwed up
        assert (0 == self.player.y)
        logging.info('Starting main loop')
        fps_clock = pygame.time.Clock()
        while True:
            self.display_surf.fill(WHITE)
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == KEYDOWN or event.type == KEYUP:
                    self.change_movement(event)
            self.update_objects()
            self.move()
            self.redraw()
            fps_clock.tick(FPS)


def run_tests():
    logging.info('Run tests')
    pygame.init()
    display_surf = pygame.display.set_mode((WINDOW_SIZE_X, WINDOW_SIZE_Y), 0, 32)
    pygame.display.set_caption("Dinosaurs Evolved")
    unittest.main()


if __name__ == '__main__':
    #run_tests()
    main = MainLoop('map_definitions/Second.xml')