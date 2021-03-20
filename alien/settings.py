import os
class Settings():
    '''储存《外星人入侵》的所有设置的类'''
    def __init__(self):
        '''初始化游戏的静态设置'''
        #屏幕设置
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (0, 0, 0)

        #飞船设置
        self.ship_limit = 2

        #子弹设置
        self.bullets_allowed = 3

        #外星人设置
        #fleet_direction为1表示向右移，为-1向左
        self.fleet_direction = 1

        #显示字体设置
        self.font = '华文行楷'
        self.font_size = 22

        #数据储存位置(伪相对位置)
        self.high_score_dir = os.getcwd() + '\\bin'
        self.high_score_file = self.high_score_dir + '\\\\high_score.txt'
        self.image_dir = os.getcwd() + '\\images\\\\ship.bmp'

        #加快游戏节奏的速度
        self.speedup_scale = 1.2

        #外星人点数提高的速度
        self.score_scale = 1.5

        #初始化动态参数
        self.initialize_dynamic_settings()

        #从文件中读取历史最高分
        self.find_high_score()
    
    def initialize_dynamic_settings(self):
        '''初始化随游戏进行而变化的设置'''
        #飞船设置
        self.ship_speed_factor = 4

        # 子弹设置
        self.bullet_speed_factor = 4

        #外星人设置
        self.alien_speed_factor = 2
        self.fleet_drop_speed = 5
        self.alien_points = 50
     

    def increase_speed(self):
        '''提高速度设置'''
        #加快游戏节奏
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale
        self.fleet_drop_speed *= self.speedup_scale
        
    def increase_score(self):
        '''提高飞船得分'''
        self.alien_points = int(self.alien_points * self.score_scale)

    def find_high_score(self):
        exist = os.path.exists(self.high_score_dir)
        if not exist:
            os.makedirs(self.high_score_dir)
            with open(self.high_score_file, 'w') as f:
                f.write(str(0))
        with open(self.high_score_file, 'r') as f:
            self.high_score = int(f.readline())
            
        
        
        
