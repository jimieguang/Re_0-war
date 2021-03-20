#第三方库
import pygame
from pygame.sprite import Group
import time

#自写py文件
from ship import Ship
from settings import Settings
import game_functions as gf
from alien import Alien
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard

def run_game():
    #初始化游戏并创建一个屏幕对象（画布）
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode(
        (ai_settings.screen_width,ai_settings.screen_height)
    )
    pygame.display.set_caption('Re_0 War')

    #创建各种按钮
    play_button = Button(ai_settings, screen, '开始游戏', -50)
    continue_button = Button(ai_settings, screen, '继续游戏', -50)
    restart_button = Button(ai_settings, screen, '重新开始', 0)
    exit_button = Button(ai_settings, screen, '退出游戏', 50)

    #创建一个用于存储游戏统计信息的实例,并创建记分牌
    stats = GameStats(ai_settings)
    sb =Scoreboard(ai_settings, screen, stats)
    #创建一艘飞船
    ship = Ship(ai_settings, screen)
    #创建一个用于存储子弹的编组
    bullets = Group()
    # #创建一个外星人（怠惰）
    # alien=Alien(ai_settings,screen)
    #创建外星人编组
    aliens = Group()
    # 创建外星人群
    gf.create_fleet(ai_settings, screen, ship, aliens)
    
    #开始游戏的主循环
    cycle_index  = 1
    while True:
        #控制游戏帧率以保证游戏在各种性能机器中以同样节奏运行(仅在第一次循环时执行)
        start = time.time()

        #监视键盘和鼠标事件
        gf.chek_events(ai_settings, screen, stats, play_button,continue_button,restart_button,exit_button, ship,aliens, bullets)
        #开始游戏
        if stats.game_active:
            #飞船事件
            ship.update()
            #子弹事件
            gf.update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets)
            #外星人事件
            gf.update_aliens(ai_settings, stats, screen, ship, aliens, bullets)
        #更新屏幕事件
        gf.update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, play_button, continue_button, restart_button, exit_button)

        #控制游戏帧率以保证游戏在各种性能机器中以同样节奏运行
        end = time.time()
        time_gap = end - start
        if time_gap <= 0.005:
            time.sleep(0.005 - time_gap)
        else:
            #设置为5是为了避免刚开始运行速度慢导致游戏出问题
            if cycle_index == 5:
                ai_settings.ship_speed_factor *= (time_gap / 0.005)
                ai_settings.alien_speed_factor *= (time_gap / 0.005)
                ai_settings.bullet_speed_factor *= (time_gap / 0.005)
            #取消执行条件
            cycle_index += 1
run_game()