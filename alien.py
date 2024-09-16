import pygame
from pygame.sprite import Sprite


class Alien(Sprite):
    '''Класс представляющий одного пришельца'''
    def __init__(self, ai_settings, screen):
        '''Инициализирует пришельца и задает его начальную позицию'''
        super(Alien, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings
        
        # Загрузка изображения пришельца и получение его прямоугольника
        self.image = pygame.image.load(r"images\alien_enemy.bmp")
        self.rect = self.image.get_rect()
        
        # Каждый пришельец появляется в левой части экрана
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height
        
        # Сохраняет абсолютную позицию пришельца
        self.x = float(self.rect.x)


    def update(self):
        '''Перемещение пришельца вправо или влево'''
        self.x += (self.ai_settings.alien_speed_factor * 
                   self.ai_settings.fleet_direction)
        self.rect.x = self.x

    def blitme(self):
        '''Рисует пришельца в текущей позиции'''
        self.screen.blit(self.image, self.rect)

    def check_edges(self):
        '''Возвращает True, если пришелец у края экрана'''
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right:
            return True
        elif self.rect.left <= 0:
            return True
