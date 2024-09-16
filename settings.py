class Settings:
    '''Класс для хранения всех настроек игры'''
    def __init__(self):
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)
        self.ship_speed_factor = 1.5
        self.ship_limit = 3
        # Параметры пули
        self.bullet_speed_factor = 5
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = 255, 0, 0
        self.bullets_allowed = 4
        self.alien_speed_factor = 1
        self.fleet_drop_speed = 5
        self.speedup_scale = 1.1
        self.score_scale = 1.5
        self.intialize_dynamic_settings()
        
    def intialize_dynamic_settings(self):
        '''Инициализирует настройки изменяющиеся в ходе игры'''
        self.ship_speed_factor = 1.5
        self.bullet_speed_factor = 3
        self.alien_speed_factor = 1
        self.fleet_direction = 1
        self.aliens_point = 50
        
    def increase_speed(self):
        '''Увеличивает настройки скорости'''
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale
        self.aliens_point = int(self.aliens_point * self.score_scale)       
