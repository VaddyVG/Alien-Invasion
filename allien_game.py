import pygame
from pygame.sprite import Group
from settings import Settings
from ship import Ship
from button import Button
from alien import Alien
from game_stats import GameStats
from scoreboard import Scoreboard
import game_functions as gf

def run_game():
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption("Alien Invasion")
    play_button = Button(ai_settings, screen, "Play")
    ship = Ship(ai_settings, screen)  # Создание корабля
    alien = Alien(ai_settings, screen)  # Создание пришельца
    bullets = Group()  # Создание группы для хранения пуль
    aliens = Group()  # Создание флота пришельцев
    gf.create_fleet(ai_settings, screen, ship, aliens)
    stats = GameStats(ai_settings)
    sb = Scoreboard(ai_settings, screen, stats)
    while True:
        gf.check_events(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets)
        if stats.game_active:
            ship.update()
            gf.bullets_update(ai_settings, screen, stats, sb, ship, aliens, bullets)
            gf.update_aliens(ai_settings, screen, stats, sb, ship, aliens, bullets)
            gf.update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, play_button)
        
        
if __name__ == "__main__":
    run_game()


