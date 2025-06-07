#关卡1   已完成
#目标：输入正确的开机密码
#本来想把密码设置成"密码"，但输入法问题似乎无法输入中文...改成password了
#同样是输入法问题，注意一切跟键盘操作相关的地方都要把输入法切换成英文，不然操作/输入不了



import pygame
from .level_base import BaseLevel
from resource_manager import res_mgr,music_manager
from config import GameState, config
from PTransition import TransitionManager

class Level1(BaseLevel):

    #此处完成所有初始化，包括需要用到的资源和变量（pygame初始化在main完成了）
    def __init__(self, screen, res_mgr):
        super().__init__(screen, res_mgr)
        self.bg = res_mgr.get_image("bg_L1")  # 背景
        self.bg_2 = res_mgr.get_image("bg_L1_2")  # 背景-欢迎
        self.mouse = res_mgr.get_image("mouse_normal")  # 鼠标
        self.screen_black = res_mgr.get_image("screen_black")  # 底图

        self.button_ok = res_mgr.get_image("button_ok")
        self.inputbox = res_mgr.get_image("inputbox")

        self.font = res_mgr.load_font("default", size=28)  # 默认字体
        self.large_font = res_mgr.load_font("large", size=72)  # 默认字体放大版

        self.effectwakeup = res_mgr.get_sound("effect_wakeup")
        
        # 密码输入框相关属性
        self.input_box = pygame.Rect(590, 650, 500, 80)  # 调整为图片尺寸
        self.input_text = ''
        self.active = False
        self.error_message = ''
        self.button_rect = pygame.Rect(775, 750, 130, 80)  # 调整为图片尺寸

        # 欢迎界面相关属性
        self.show_welcome = False
        self.welcome_start_time = 0
        self.welcome_duration = 1000  # 等待1秒

        self.transition_over = False
        
        # 过渡管理器
        self.transition = TransitionManager(1680, 960)

        self.prompt_text = ''

        self.color_text=(100,0,80)

    def handle_keydown(self, event):
        if not self.show_welcome:
            if self.active:  # 激活输入框后
                if event.key == pygame.K_RETURN:  # 确认键点击
                    self.check_password()
                elif event.key == pygame.K_BACKSPACE:
                    self.input_text = self.input_text[:-1]
                else:
                    self.input_text += event.unicode  # 逐位记录输入密码

    def handle_mouse_button_down(self, event):
        if not self.show_welcome:
            # 检查是否点击了输入框
            if self.input_box.collidepoint(event.pos):
                self.active = True
                self.error_message = ''
            else:
                self.active = False
        
            # 检查是否点击了确认按钮
            if self.button_rect.collidepoint(event.pos):
                self.check_password()
    
    def check_password(self):
        # 检查输入的密码是否正确
        if self.input_text == "password":  # 这里设置正确密码
            self.show_welcome = True
            self.welcome_start_time = pygame.time.get_ticks()
            self.input_text = ''
            self.effectwakeup.play()
        else:
            self.error_message = "error"

    def update(self):
        super().update()
        self.transition_over = self.transition.update()
        # 检查欢迎界面是否应该结束
        if self.show_welcome and not self.transition.is_active():
            current_time = pygame.time.get_ticks()
            if current_time - self.welcome_start_time >= self.welcome_duration:
                # 开始淡入过渡效果，完成后切换到下一个关卡
                self.transition.start(duration=500)
        if self.transition_over:
            self.show_welcome = False
            config.current_state = GameState.LEVEL2
            music_manager.play_bgm("bgm_normal")
            self.transition_over = False

    def draw(self):
        self.screen.fill((0, 0, 0))

        if not self.show_welcome:
            # 绘制正常界面
            self.screen.blit(self.bg, (200, 0))
            
            # 在输入框上方绘制提示文本
            prompt_text = self.font.render("Please enter the password:", True, self.color_text)
            self.screen.blit(prompt_text, (self.input_box.x, self.input_box.y - 30)) 

            # 绘制输入框图片
            self.screen.blit(self.inputbox, (self.input_box.x, self.input_box.y))
            
            # 绘制输入的密码
            text_surface = self.font.render(self.input_text, True, self.color_text)
            self.screen.blit(text_surface, (self.input_box.x + 270, self.input_box.y + 25))
            
            # 绘制确认按钮图片
            self.screen.blit(self.button_ok, (self.button_rect.x, self.button_rect.y))
        
            # 绘制错误信息
            if self.error_message and config.current_state == GameState.LEVEL1:
                error_text = self.font.render(self.error_message, True, (255, 0, 0))
                self.screen.blit(error_text, (self.input_box.x, self.input_box.y + 80))
        else:
            # 绘制欢迎界面
            self.screen.blit(self.bg_2, (200, 0))

            
            # 绘制过渡效果
            self.transition.draw(0, 0, self.screen)

        # 绘制鼠标指针
        x, y = pygame.mouse.get_pos()
        self.screen.blit(self.mouse, (x-4, y-4))

        if config.current_state == GameState.LEVEL2:  # 防止过渡完成后原场景会闪现一下
            self.screen.fill((0, 0, 0))

        # 绘制暗角效果
        self.screen.blit(self.screen_black, (0, 0))