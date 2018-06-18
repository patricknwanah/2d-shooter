from PythonApplication3 import *
import unittest

class TestPlayerFunctions(unittest.TestCase):
    
    def setUp(self):
        pygame.init()
        size = [SCREEN_WIDTH, SCREEN_HEIGHT]
        screen = pygame.display.set_mode(size)
        self.player = Player()
        self.player.level = Level(self.player)
    
    def ReInit(self):     #call at the start of each test to reset movement-related variables as some test will change them.
        self.player.x = 0
        self.player.y = 0
        self.player.change_x = 0
        self.player.change_y = 0
        self.direction = "R"
    
    def test_LeftSpriteLoad(self):     #did the correct number of frames load for the left sprite?
        spritelen = len(self.player.left_frames)
        self.assertEqual(spritelen, 5)
    
    def test_RightSpriteLoad(self):     #did the correct number of frames get applied to the right sprite?
        spritelen = len(self.player.right_frames)
        self.assertEqual(spritelen, 5)
    
    def test_GravInAir(self):     #is gravity applied in air?
        self.ReInit()
        self.player.calc_grav()
        self.assertTrue((self.player.change_y>0))
    
    def test_GravOnGround(self):     #is gravity not applied while on the ground?
        self.ReInit()
        self.player.rect.y = SCREEN_HEIGHT
        self.player.calc_grav()
        self.assertEqual(self.player.change_y, 0)
    
    def test_JumpInAir(self):     #Will the player not jump while in the air?
        self.ReInit()
        self.player.jump()
        self.assertEqual(self.player.change_y, 0)
    
    def test_JumpOnGround(self):     #Will the player jump while on the ground?
        self.ReInit()
        self.player.rect.y = SCREEN_HEIGHT
        self.player.jump()
        self.assertTrue((self.player.change_y<0))


if __name__=="__main__":
    unittest.main()