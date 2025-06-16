#结束画面

import pygame
from .level_base import BaseLevel
from config import GameState, config

class Level15(BaseLevel):

    def __init__(self, screen, res_mgr):
        super().__init__(screen, res_mgr)
        self.screen_black = res_mgr.get_image("screen_black")  # 黑色底图
        self.font = res_mgr.load_font("large", size=72)  # 大号字体
        
        # 文字淡入效果相关变量
        self.text_alpha = 0  # 文字透明度
        self.fade_speed = 1  # 淡入速度
        self.show_text = False  # 是否显示文字
        
        # 过渡管理器
        from PTransition import TransitionManager
        self.transition = TransitionManager(1680, 960)

    def handle_keydown(self, event):
        pass

    def handle_mouse_button_down(self, event):
        pass
    
    def update(self):
        super().update()
        
        # 控制文字淡入效果
        if self.show_text and self.text_alpha < 255:
            self.text_alpha += self.fade_speed
        elif not self.show_text and self.text_alpha > 0:
            self.text_alpha -= self.fade_speed
            
        # 开始显示文字
        if not self.show_text:
            self.show_text = True

    def draw(self):
        # 绘制黑色背景
        self.screen.fill((0, 0, 0))
        self.screen.blit(self.screen_black, (0, 0))
        
        # 绘制淡入的END文字
        if self.text_alpha > 0:
            text_surface = self.font.render("END", True, (255, 255, 255))
            text_surface.set_alpha(self.text_alpha)
            text_rect = text_surface.get_rect(center=(self.screen.get_width()//2, 
                                                     self.screen.get_height()//2))
            self.screen.blit(text_surface, text_rect)
