from import_all import *

class GenericAnimal(GenericTimedSurface):
    """ Contains the basic mechanisms for animals, namely health and mass """
    def __init__(self, max_health, current_size, level_list, attack_min, attack_max, width, height, base_color, x=0, y=0, timer=0):
        super(GenericAnimal, self).__init__(timer, width, height, base_color, x, y)
        self.max_health = max_health
        self.current_health = max_health
        self.current_mass = 0
        self.level = current_size
        self.level_list = level_list
        self.attack_min = attack_min
        self.attack_max = attack_max
        
    def __repr__(self):
        s = super(GenericAnimal, self).__repr__()
        return 'GenericAnimal(max_health=%r, level=%r, level_list=%r, attack_min=%r, attack_max=%r)||%s' % (self.max_health, self.level, self.level_list, self.attack_min, self.attack_max, s)
        
    def __str__(self):
        s = super(GenericAnimal, self).__str__()
        return 'GenericAnimal-max_health:{0} level:{1} level_list:{2} attack_min:{3} attack_max{4}||{5}'.format(self.max_health, self.level, self.level_list, self.attack_min, self.attack_max, s)
    
    def eat_food(self, food_qty):
        """ Food will first regen health, and then if any is left over add it to mass """
        if(food_qty > 0):
            if(self.current_health != self.max_health):
                dif = self.max_health - self.current_health
                if(dif >= food_qty):
                    self.current_health += food_qty
                    food_qty = 0
                else:
                    self.current_health = self.max_health
                    food_qty -= dif
            self.current_mass += food_qty
            if(self.level < len(self.level_list) and self.level_list[self.level] <= self.current_mass):
                self.level += 1
                self.level_up()
                logging.info('Level up! New level {0}'.format(self.level))
            print("health {0} mass {1}".format(self.current_health, self.current_mass))
    
    def attack(self):
        """ Return the attack damage"""
        return random.randrange(self.attack_min, self.attack_max)
    
    def take_damage(self, damage):
        """ Take damage, return if dead """
        self.current_health -= damage
        if(self.current_health <= 0):
            return False
        return True
    
    def get_health(self):
        """ Return the current and max health """
        return self.current_health, self.max_health
    
    def get_mass(self):
        """ Return current mass """
        return self.current_mass
    
    def get_size(self):
        """ Return current size """
        return self.size_level
    
    def level_up(self):
        print('Leveled up to {0}!!'.format(self.level))

class AnimalsTests(unittest.TestCase):
    """ unit tests for animals """
    def setUp(self):
        pygame.init()
        self.animal = GenericAnimal(100, 1, [100, 200], 10, 50, 0,0, RED)
        self.animal.current_health = 80
    
    def tearDown(self):
        self.animal = None
        
    def testNoFood(self):
        self.animal.eat_food(0)
        current_health, max_health = self.animal.get_health()
        self.assertEqual(max_health, self.animal.max_health, "Somehow max health changed")
        self.assertEqual(current_health, 80, "Did not add a little health")
        self.assertEqual(self.animal.get_mass(), 0, "Mass was added when it should not")
        
    def testSomeHealth(self):
        self.animal.eat_food(10)
        current_health, max_health = self.animal.get_health()
        self.assertEqual(max_health, self.animal.max_health, "Somehow max health changed")
        self.assertEqual(current_health, 90, "Did not add a little health")
        self.assertEqual(self.animal.get_mass(), 0, "Mass was added when it should not")
    
    def testAllHealth(self):
        self.animal.eat_food(20)
        current_health, max_health = self.animal.get_health()
        self.assertEqual(max_health, self.animal.max_health, "Somehow max health changed")
        self.assertEqual(current_health, 100, "Did not add a little health")
        self.assertEqual(self.animal.get_mass(), 0, "Mass was added when it should not")
        
    def testHealthAndMass(self):
        self.animal.eat_food(50)
        current_health, max_health = self.animal.get_health()
        self.assertEqual(max_health, self.animal.max_health, "Somehow max health changed")
        self.assertEqual(current_health, 100, "Did not add a little health")
        self.assertEqual(self.animal.get_mass(), 30, "Wrong mass added")
        
    def testOnlyAddMass(self):
        self.animal.current_health = self.animal.max_health
        self.animal.eat_food(50)
        current_health, max_health = self.animal.get_health()
        self.assertEqual(max_health, self.animal.max_health, "Somehow max health changed")
        self.assertEqual(current_health, 100, "Wrong Health")
        self.assertEqual(self.animal.get_mass(), 50, "Wrong Mass")
    
    def testLevelUp(self):
        self.animal.current_health = self.animal.max_health
        self.animal.eat_food(100)
        self.assertEqual(self.animal.get_mass(), 100, "Wrong Mass")
        self.assertEqual(self.animal.level, 1, "Wrong Level")
        self.animal.eat_food(200)
        self.assertEqual(self.animal.get_mass(), 300, "Wrong Mass")
        self.assertEqual(self.animal.level, 2, "Wrong Level")
        self.animal.eat_food(200)
        self.assertEqual(self.animal.get_mass(), 500, "Wrong Mass")
        self.assertEqual(self.animal.level, 2, "Wrong Level")
        
    def testTakeDamage(self):
        self.animal.current_health = self.animal.max_health
        ret = self.animal.take_damage(50)
        self.assertEqual(self.animal.current_health, 50, "Wrong Health")
        self.assertTrue(ret, "Should not be dead")
        ret = self.animal.take_damage(50)
        self.assertEqual(self.animal.current_health, 0, "Wrong Health")
        self.assertFalse(ret, "Not dead")
        
    def testAttack(self):
        dam = self.animal.attack()
        self.assertGreaterEqual(dam, self.animal.attack_min, "Attack too low")
        self.assertGreaterEqual(self.animal.attack_max, dam, "Attack too high")