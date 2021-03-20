import pygame.font

class Button():
    
    def __init__(self, ai_settings, screen, msg, adjust_y=0):
        '''初始化按钮的属性'''
        self.screen = screen
        self.screen_rect = screen.get_rect()
        
        #设置按钮的尺寸和其他属性
        self.width, self.height = 200, 50
        self.button_color = (255, 255, 255)
        self.text_color = (0, 0, 0)
        self.font = pygame.font.SysFont(ai_settings.font, ai_settings.font_size + 12)

        #对按钮的垂直位置进行调整
        self.adjust_y = adjust_y
        
        #创建按钮的rect对象，并使其居中
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = (self.screen_rect.centerx, self.screen_rect.centery + self.adjust_y)

        # 按钮的标签仅需创建一次
        self.prep_msg(msg)

        

    def prep_msg(self, msg):
        '''将msg渲染成图像，并使其在按钮上居中'''
        self.msg_image = self.font.render(msg, True, self.text_color,
                        self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        #添加位置调整的按钮位置
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        #绘制一个用颜色填充的按钮，再绘制文本
        # self.screen.fill(self.button_color, self.rect)  #美观起见，注释掉
        self.screen.blit(self.msg_image, self.msg_image_rect)
