import sys
import pygame
from bullet import Bullet
from alien import Alien
from time import sleep

def check_keydown_events(event, ai_settings, screen, ship, bullets):
    '''Реагирует на нажатие клавиш'''
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    # Создание новой пули и включение её в группу bullets
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings, screen, ship, bullets)
    elif event.key == pygame.K_q:
        sys.exit()

                  
def fire_bullet(ai_settings, screen, ship, bullets):
    '''Выпускает новую пулю, если максимум не достигнут'''
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)


def check_keyup_events(event, ship):
    '''Реагирует на отпускание клавиш'''
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False
        

def check_events(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets):
    '''Обрабатывает нажатие клавиш и мыши'''
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, ship, bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, stats, sb, play_button, ship,
                              aliens, bullets, mouse_x, mouse_y)
            
            
def check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens,
 bullets, mouse_x, mouse_y):
    '''Запускает новую игру при нажатии кнопки Play'''
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        ai_settings.intialize_dynamic_settings()
        pygame.mouse.set_visible(False)
        stats.reset_stats()
        stats.game_active = True
        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()
        sb.prep_ships()
        aliens.empty()
        bullets.empty()
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()
                 

def update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, play_button):  # Обновляет изображение на экране и отображает новый
    screen.fill(ai_settings.bg_color)
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.blitme()
    aliens.draw(screen)
    sb.show_score()
    if not stats.game_active:
        play_button.draw_button()
    pygame.display.flip()

     
    
def bullets_update(ai_settings, screen, stats, sb, ship, aliens, bullets):
    '''Обновляет позиции пуль и уничтожает старые'''
    bullets.update()
    for bullet in bullets.copy():
            if bullet.rect.bottom <= 0:
                bullets.remove(bullet)
    check_bullet_collision(ai_settings, screen, stats, sb, ship, aliens, bullets)


def check_bullet_collision(ai_settings, screen, stats, sb, ship, aliens, bullets):
    '''Обработка колизий пуль с пришельцами'''
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
    if collisions:
        for alien in collisions.values():
            stats.score += ai_settings.aliens_point * len(alien)
        sb.prep_score()
        check_high_score(stats, sb)
    if len(aliens) == 0:
        bullets.empty()
        ai_settings.increase_speed()
        stats.level += 1
        sb.prep_level()
        create_fleet(ai_settings, screen, ship, aliens)
                

def create_fleet(ai_settings, screen, ship, aliens):
    '''Создает флот пришельцев'''
    alien = Alien(ai_settings, screen)
    numbers_aliens_x = get_number_aliens(ai_settings, alien.rect.width)
    number_rows = get_number_rows(ai_settings, ship.rect.height, alien.rect.height)
    
    # Создание первого ряда пришельцев
    for row_number in range(number_rows):
        for alien_number in range(numbers_aliens_x):
            create_alien(ai_settings, screen, aliens, alien_number, row_number)

        
def get_number_aliens(ai_settings, alien_width):
    '''Вычисляет количество пришельцев в ряду'''
    available_space_x = ai_settings.screen_width - 2 * alien_width
    numbers_aliens_x = int(available_space_x / (2 * alien_width))
    return numbers_aliens_x


def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    '''Создает пришельца и размещает его в ряду'''
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)
    
    
def get_number_rows(ai_settings, screen_height, alien_height):
    '''Вычисляет количество рядов'''
    available_space_y = ai_settings.screen_height - 3 * alien_height - screen_height
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows


def check_fleet_edges(ai_settings, aliens):
    '''Реагирует на достижение пришельцем края экрана'''
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break


def change_fleet_direction(ai_settings, aliens):
    '''Опускает весь флот и меняет направление флота'''
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1
    

def check_alliens_bottom(ai_settings, screen, stats, sb, ship, aliens, bullets):
    '''Проверяет, добрались ли пришельцы до нижнего края экрана'''
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets)
            break
        

def update_aliens(ai_settings, screen, stats, sb, ship, aliens, bullets):
    '''Проверяет достиг ли флот края экрана,
    после чего обновляет позиции всех пришельцев во флоте'''
    check_fleet_edges(ai_settings, aliens)
    aliens.update()
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets)
    check_alliens_bottom(ai_settings, screen, stats, sb, ship, aliens, bullets)
        
        
def ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets):
    '''Обрабатывает столкновение корабля с пришельцем'''
    if stats.ships_left > 0:
        stats.ships_left -= 1
        sb.prep_ships()
        aliens.empty()
        bullets.empty()
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()
        sleep(0.5)
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)
        
        
def check_high_score(stats, sb):
    '''Проверяет новый рекорд'''
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()
    
        