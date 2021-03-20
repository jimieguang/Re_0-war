import sys
import pygame
from time import sleep

from bullet import Bullet
from alien import Alien


def chek_kerdown_events(event, ai_settings, screen, stats, ship, bullets):
    '''响应按键'''
    if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
        #向右移动飞船
        ship.moving_right = True
    if event.key == pygame.K_LEFT or event.key == pygame.K_a:
        #向左移动飞船
        ship.moving_left = True
    if event.key == pygame.K_UP or event.key == pygame.K_w:
        #向上移动飞船
        ship.moving_up = True
    if event.key == pygame.K_DOWN or event.key == pygame.K_s:
        #向下移动飞船
        ship.moving_down = True
    elif event.key == pygame.K_SPACE:
        #发射子弹
        fire_bullets(ai_settings, screen, ship, bullets)
    #游戏活动状态下，进入暂停界面
    elif event.key == pygame.K_ESCAPE and stats.game_active:
        stats.game_active = False
        stats.pause_active = True
        pygame.mouse.set_visible(True)
        


def chek_keyup_events(event, ship):
    '''响应松开按键'''
    if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
        ship.moving_right = False
    if event.key == pygame.K_LEFT or event.key == pygame.K_a:
        ship.moving_left = False
    if event.key == pygame.K_UP or event.key == pygame.K_w:
        ship.moving_up = False
    if event.key == pygame.K_DOWN or event.key == pygame.K_s:
        ship.moving_down = False
    
    


def chek_events(ai_settings, screen, stats, play_button,continue_button,restart_button, exit_button, ship,aliens, bullets):
    '''响应按键和鼠标事件'''
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            chek_kerdown_events(event, ai_settings, screen, stats, ship, bullets)
        elif event.type == pygame.KEYUP:
            chek_keyup_events(event, ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_button(ai_settings, stats, screen, ship, aliens, bullets, play_button,continue_button, restart_button, exit_button, mouse_x, mouse_y)

def chek_fleet_edges(ai_settings, aliens):
    '''响应外星人到达边缘事件'''
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break

def check_bullet_alien_collisions(ai_settings, screen,stats,sb, ship, aliens, bullets):
    #检测碰撞的子弹和外星人，以字典的形式存储并删除实例对象
    #ps：其中第一个true表示删除子弹，第二个表示删除外星人
    collisions= pygame.sprite.groupcollide(bullets, aliens, True, True)
    if collisions:
        for aliens in collisions.values():
            stats.score += ai_settings.alien_points*len(aliens)
            sb.prep_score()
        check_high_score(stats, sb)
    if len(aliens) == 0:
        #删除现有子弹，并新建一群外星人
        bullets.empty()
        #提高等级，加快游戏节奏
        stats.level += 1
        sb.prep_level()
        ai_settings.increase_speed()
        ai_settings.increase_score()
        create_fleet(ai_settings, screen, ship, aliens)

def check_aliens_bottom(ai_settings, stats, screen, ship, aliens, bullets):
    '''检查是否有外星人到达屏幕边缘'''
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            #像飞船被撞到一样进行处理
            end_start(ai_settings, stats, screen, ship, aliens, bullets)
            break

def check_button(ai_settings, stats,screen, ship, aliens, bullets, play_button, continue_button, restart_button, exit_button, mouse_x, mouse_y):
    '''在玩家单击按钮时发生相应变化'''
    #该方法检测鼠标是否与按钮矩形发生‘碰撞’
    #非暂停非活动状态下，单击play开始新游戏，将鼠标设为不可视
    if play_button.rect.collidepoint(mouse_x, mouse_y) and not stats.pause_active and not stats.game_active:
        stats.game_active = True
        pygame.mouse.set_visible(False)
        #清空外星人列表和子弹列表
        aliens.empty()
        bullets.empty()
        #创建一群新的外星人，并将飞船放到屏幕底端中央
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()

    #暂停状态下，单击continue继续游戏，不改变原有信息
    if continue_button.rect.collidepoint(mouse_x, mouse_y) and stats.pause_active:
        stats.game_active = True
        pygame.mouse.set_visible(False)

    #暂停状态下，单击restart重新开始游戏
    if restart_button.rect.collidepoint(mouse_x, mouse_y) and stats.pause_active:
        #触发死亡事件
        stats.ships_left = 0
        end_start(ai_settings, stats, screen, ship, aliens, bullets)
        #重置页面显示，和非暂停状态点击play行为一致
        stats.game_active = True
        pygame.mouse.set_visible(False)
        #清空外星人列表和子弹列表
        aliens.empty()
        bullets.empty()
        #创建一群新的外星人，并将飞船放到屏幕底端中央
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()

    #暂停状态下，单击exit结束游戏
    if exit_button.rect.collidepoint(mouse_x, mouse_y) and stats.pause_active:
        sys.exit()


def check_high_score(stats, sb):
    '''检查是否诞生了最高分'''
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()


def update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, play_button,continue_button, restart_button, exit_button):
    '''更新屏幕上的图像，并切换到新屏幕'''
    #每次循环时都重绘屏幕
    screen.fill(ai_settings.bg_color)
    #在飞船和外星人后面重绘所有子弹
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.blitme()
    #绘制外星人
    aliens.draw(screen)
    #显示得分
    #本代码试图在开启新游戏时归零得分，会降低效率但必不可少
    if stats.game_active:
        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()
        sb.prep_ship()
    sb.show_score()
    #如果游戏处于非活动且非暂停状态，就绘制play按钮
    if not stats.game_active and not stats.pause_active:
        play_button.draw_button()
    #如果游戏处于非活动且暂停状态，绘制暂停页面
    if not stats.game_active and stats.pause_active:
        continue_button.draw_button()
        restart_button.draw_button()
        exit_button.draw_button()

    #让最近绘制的屏幕可见
    pygame.display.flip()

def update_bullets(ai_settings, screen, ship, stats, sb, aliens, bullets):
    '''更新子弹的位置，并删除已消失的子弹'''
    #更新子弹位置
    bullets.update()
    #删除屏幕外的子弹
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    #删除击中外星人的子弹
    check_bullet_alien_collisions(ai_settings, screen, ship, stats, sb, aliens, bullets)

def update_aliens(ai_settings, stats, screen, ship, aliens, bullets):
    '''检测是否有外星人位于屏幕边缘，并更新整群外星人的位置'''
    chek_fleet_edges(ai_settings, aliens)
    aliens.update()
    #检测外星人和飞船之间的碰撞
    if pygame.sprite.spritecollideany(ship, aliens):
        end_start(ai_settings, stats, screen, ship, aliens, bullets)
    #检查是否有外星人到达屏幕底端
    check_aliens_bottom(ai_settings, stats, screen, ship, aliens, bullets)

def end_start(ai_settings, stats, screen, ship, aliens, bullets):
    '''响应死亡事件，并初始化参数为新游戏做准备'''
    if stats.ships_left > 0:
        #将ships_left减1
        stats.ships_left -= 1
        #清空外星人列表和子弹列表
        aliens.empty()
        bullets.empty()
        #创建一群新的外星人，并将飞船放到屏幕底端中央
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()
        #暂停
        sleep(0.5)
    else:
        #存储最高分(如果产生的话)
        if stats.score == stats.high_score:
            with open(ai_settings.high_score_file, 'w') as f:
                f.write(str(stats.score))
        #初始化游戏
        stats.game_active = False
        stats.pause_active = False
        stats.reset_stats()
        ship.center_ship()
        #显示鼠标
        pygame.mouse.set_visible(True)
        #重置游戏动态设置
        ai_settings.initialize_dynamic_settings()
    
    
        



def fire_bullets(ai_settings, screen, ship, bullets):
    '''如果没有达到限制，就发射一枚子弹'''
    #创建一颗子弹，并将其加入到编组bullets中
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullets = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullets)

def get_number_aliens(ai_settings, alien_width):
    '''计算每行可容纳多少外星人'''
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x

def get_number_rows(ai_settings, ship_height, alien_height):
    '''计算屏幕可容纳多少行外星人'''
    available_space_y = (ai_settings.screen_height - 4 * alien_height - ship_height)
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows

def change_fleet_direction(ai_settings, aliens):
    '''将整个外星人群下移，并改变其移动方向'''
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1

def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    '''创建一个外星人并将其放在当前行'''
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    # +50是为了使外星人不与命数等图标重合
    alien.rect.y = 50 + alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)


def create_fleet(ai_settings, screen, ship, aliens):
    '''创建外星人群'''
    #创建一个外星人，并计算一行可容纳多少个外星人
    #外星人间距为外星人宽度
    alien = Alien(ai_settings, screen)
    number_aliens_x = get_number_aliens(ai_settings, alien.rect.width)
    number_rows = get_number_rows(ai_settings, ship.rect.height, alien.rect.height)
    
    # 创建外星人群
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(ai_settings, screen, aliens, alien_number, row_number)
        
    

