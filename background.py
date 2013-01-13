from import_all import *
from scenery import *
from map import Map

class Background(GenericSurface):
    """Pretty much everything but the player
    
    The background will encomapse most of the objects in the game. The lowest level is the surface,
    which will appear only as the area that the player can not walk on that ring the map. The 
    playable_surface is everything that the player can move on, and will also be the place
    where all the scenery and enemies are placed.  All of these objects should be placed into the 
    all_objects list so they can be accessed for collision checks among other things
    
    """
    def __init__(self, file_name):
        self.map = Map(file_name)
        super(Background, self).__init__(self.map.BACKGROUND_DIMENSION_X, self.map.BACKGROUND_DIMENSION_Y, BLUE)
        self.create_background()
        self.draw_all()
        
    def draw_all(self):
        """ Draw everything from scratch """
        self.all_objects = []
        self.add_objects()
        self.display_object()
        self.surface.blit(self.playable_surface, (OFFSET_X, OFFSET_Y))
        
    def create_background(self, box_dim = 100, background_color = WHITE, box_color = BLACK):
        """ Used to draw the playable_surface """
        self.playable_surface = pygame.Surface((self.map.PLAYABLE_DIMENSION_X, self.map.PLAYABLE_DIMENSION_Y))
        self.playable_surface = self.playable_surface.convert_alpha()
        self.playable_surface.fill(background_color)
        assert(self.map.PLAYABLE_DIMENSION_X % box_dim == 0)
        assert(self.map.PLAYABLE_DIMENSION_Y % box_dim == 0)
        number_boxes_x = self.map.PLAYABLE_DIMENSION_X/box_dim
        number_boxes_y = self.map.PLAYABLE_DIMENSION_Y/box_dim
        draw = True
        for y in range(number_boxes_y):
            for x in range(number_boxes_x):
                if(draw):
                    pygame.draw.rect(self.playable_surface, box_color, (x*box_dim, y*box_dim, box_dim, box_dim))
                draw = not draw
            draw = not draw
        
    def add_objects(self, tree_number=5):
        """Add all the objects onto the board, this includes scenery and enemies """
        for obj in self.map.objects:
            self.all_objects.append(obj)
    
        
    def display_object(self):
        """ Loop through all objects and put them on the surface """
        for current_object in self.all_objects:
            if(current_object.should_redraw_surface()):
                self.playable_surface.blit(current_object.get_surface(), (current_object.x, current_object.y))
                current_object.set_change(False)
    
    def get_objects(self):
        """ Return all the objects on the board """
        return self.all_objects
    
    def get_playable_surface(self):
        """ Return just the playable_surface, instead of the entire surface """
        return self.playable_surface
    
    def add_object(self, obj):
        """ Add a surface object to the list """
        assert(isinstance(obj, GenericSurface)) 
        self.all_objects.append(obj)
    
    def redraw(self):
        self.display_object()
        self.surface.blit(self.playable_surface, (OFFSET_X, OFFSET_Y))