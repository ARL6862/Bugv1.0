# 过渡效果
import pygame
from resource_manager import res_mgr
#使用方法：初始化处实例化过渡管理器 self.transition = TransitionManager(1680, 960)
#update       （bool）=self.transition.update()      bool控制过渡是否完成
#             if 开始过渡条件: self.transition.start(duration=500)
            #if 过渡完成 下一步
#draw       if 条件：self.transition.draw(0, 0, self.screen)







class TransitionManager:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.overlay = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)
        self.transition_active = False
        self.transition_start_time = 0
        self.transition_duration = 0
        self.transition_percent = 0.0
        self.transition_callback = None
        self.transition_over=False

        self.display_text = ""
        self.text_display_start_time = 0
        self.text_display_duration = 1500  
        self.is_showing_text = False
        self.font = res_mgr.load_font("large", size=64)
        
    def start(self, duration,text=""):
        self.transition_active = True
        self.transition_start_time = pygame.time.get_ticks()
        self.transition_duration = duration
        self.transition_percent = 0.0
        self.display_text = text
        self.is_showing_text = False
        
    def update(self):
        if self.transition_active:
            current_time = pygame.time.get_ticks()
            elapsed = current_time - self.transition_start_time
            self.transition_percent = min(elapsed / self.transition_duration, 1.0)
            
            if self.transition_percent >= 1.0:
                # 过渡完成，开始显示文本（如果有）
                if self.display_text and not self.is_showing_text:
                    self.is_showing_text = True
                    self.text_display_start_time = current_time
                elif not self.display_text or (current_time - self.text_display_start_time >= self.text_display_duration):
                    # 文本显示完成或不需要显示文本
                    self.transition_active = False
                    self.transition_over = True
                    return True

        return False



    def draw(self, color, mode, screen):  #color 0=black 1=white 2=red    mode 0=变黑 1=黑变透明
        if mode == 0:
            alpha = int(self.transition_percent * 255)
        elif mode == 1:
            alpha = int((1 - self.transition_percent) * 255)
            
        if self.transition_active or self.is_showing_text:
            if color == 0:
                self.overlay.fill((0, 0, 0, alpha))
            elif color == 1:
                self.overlay.fill((255, 255, 255, alpha))
            elif color == 2:
                self.overlay.fill((255, 0, 0, alpha))
            screen.blit(self.overlay, (0, 0))
            
            # 绘制文本（在完全黑屏后）
            if self.is_showing_text and alpha == 255:
                text_surface = self.font.render(self.display_text, True, (255, 255, 255))
                text_rect = text_surface.get_rect(center=(self.screen_width//2, self.screen_height//2))
                screen.blit(text_surface, text_rect)



    def is_active(self):
        return self.transition_active or self.is_showing_text
    






class FadeEffect:
    def __init__(self, image, pos):
        """
        基础图像效果类
        
        参数:
        - image: 要显示的图片(Surface对象)
        - pos: 图片左上角位置(x, y)
        """
        self.original_image = image
        self.image = image.copy()  # 创建副本用于修改alpha
        self.pos = pos
        self.current_time = 0
        self.finished = False
        self.active = False
        
    def start(self):
        """激活效果"""
        self.current_time = 0
        self.finished = False
        self.active = True
        
    def update(self, dt):
        """更新效果状态"""
        if not self.active or self.finished:
            return
            
        self.current_time += dt
        self._update_effect()
        
    def draw(self, screen):
        """绘制图片"""
        if self.active and not self.finished:
            screen.blit(self.image, self.pos)
    
    def is_finished(self):
        """检查效果是否已完成"""
        return self.finished
    
    def reset(self):
        """重置效果"""
        self.current_time = 0
        self.finished = False
        self.active = False

class FadeIn(FadeEffect):
    def __init__(self, image, pos, fade_time):
        super().__init__(image, pos)
        self.fade_time = fade_time
        self.image.set_alpha(0)  # 初始完全透明
        
    def _update_effect(self):
        progress = min(1.0, self.current_time / self.fade_time)
        alpha = int(255 * progress)
        self.image.set_alpha(alpha)
        
        if progress >= 1.0:
            self.finished = True

class FadeOut(FadeEffect):
    def __init__(self, image, pos, fade_time):
        super().__init__(image, pos)
        self.fade_time = fade_time
        self.image.set_alpha(255)  # 初始完全不透明
        
    def _update_effect(self):
        progress = min(1.0, self.current_time / self.fade_time)
        alpha = int(255 * (1.0 - progress))
        self.image.set_alpha(alpha)
        
        if progress >= 1.0:
            self.finished = True