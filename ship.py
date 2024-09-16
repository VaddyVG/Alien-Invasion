import pygame
from pygame.sprite import Sprite


class Ship(Sprite):
    def __init__(self, ai_settings, screen):
        '''Инициализирует корабль и его начальную позицию'''
        super(Ship, self).__init__()
        self.screen = screen 
        self.ai_settings = ai_settings
        self.image = pygame.image.load(r"images\ship.bmp")  # Изображение корабля
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()
        # Каждый корабль появляется у нижнего края экрана
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom
        self.center = float(self.rect.centerx)  # Сохранение вещественной координаты центра корабля
        self.moving_right = False  # Флаг перемещения
        self.moving_left = False


    def update(self):
        '''Обновляет позицию корабля с учетом флагов'''  
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.center += self.ai_settings.ship_speed_factor
        if self.moving_left and self.rect.left > 0:
            self.center -= self.ai_settings.ship_speed_factor
        self.rect.centerx = self.center


    def blitme(self):
        '''Рисует корабль в текущей позиции'''
        self.screen.blit(self.image, self.rect)


    def center_ship(self):
        '''Размещает корабль в центре нижней стороны'''
        self.center = self.screen_rect.centerx
