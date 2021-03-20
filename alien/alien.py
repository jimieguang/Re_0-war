import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    '''表示单个外星人的类'''
    def __init__(self, ai_settings, screen):
        '''初始化外星人并设置其初始位置'''
        super().__init__()
        self.screen = screen
        self.ai_settings = ai_settings
        
        #加载外星人图像，并设置其rect属性
        self.image = pygame.image.load('images/alien.bmp')
        self.image_sp = pygame.image.load('images/alien_sp.bmp')
        self.rect = self.image.get_rect()
        self.rect_sp = self.image_sp.get_rect()
        
        #每个外星人最初都在屏幕左上角附近
        self.rect.x = self.rect.width
        self.rect_sp.x = self.rect_sp.width
        self.rect.y = self.rect.height
        self.rect_sp.y = self.rect_sp.height

        #存储外星人的准确位置
        self.x = float(self.rect.x)
        self.x_sp=float(self.rect_sp.x)
        
    def blitme(self):
        '''在指定位置绘制外星人'''
        self.screen.blit(self.image, self.rect)
        
    def blitme_sp(self):
        '''在指定位置绘制特殊外星人'''
        self.screen.blit(self.image_sp, self.rect_sp)

    def update(self):
        '''平行移动外星人'''
        self.x += (self.ai_settings.alien_speed_factor *
                        self.ai_settings.fleet_direction)
        self.rect.x = self.x

    def check_edges(self):
        '''如果外星人位于屏幕边缘，就返回ture'''
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right:
            return True
        elif self.rect.left <= 0:
            return True

        