#真结局文本
#渐显效果已完成 用图片代替文案吧




import pygame
from Papp_window import AppIcon,StateBox,TemperatureBall,PasswordWindow
from PRightClickMenu import ContextMenu
from .level_base import BaseLevel
import PDialog
from PTransition import TransitionManager,FadeIn, FadeOut
from config import GameState, config
from resource_manager import music_manager

class Level14(BaseLevel):
    def __init__(self, screen, res_mgr):
        super().__init__(screen, res_mgr)

        self.mouse=res_mgr.get_image("mouse_normal")
        self.bg = res_mgr.get_image("bg_normal")
        self.bgside = res_mgr.get_image("bgside_normal")


        #对话控制相关参数
        self.textNum=0#当前对话段的文本序号（例如①bug：111 ②Player：222 ③bug：333...）
        self.dialogNum=1#对话段序号（例如段①：游戏开始时；段②：新手教程时；段③：游戏结束时）
        self.gameMode = 1   #0=normal;1=dialog，用这个变量来控制当前是游戏模式or剧情模式（玩家不可进行鼠标点击推进对话外的操作，bug也不会乱跑）
        self.last_played_textNum = -1  # 记录上一次播放音效的文本编号，用来控制音效免得在循环中反复播放

        
        # 图像过渡状态控制
        self.transition_state = "bg_fade_in"  # 初始状态
        self.waiting_for_click = False
        
        # 创建各个过渡效果
        self.bg_fade_in = FadeIn(self.bg, (0, 0), 2.0)  # bg渐显2秒
        self.bg_fade_out = FadeOut(self.bg, (0, 0), 2.0)  # bg渐隐2秒
        self.bgside_fade_in = FadeIn(self.bgside, (0, 0), 2.0)  # bgside渐显2秒
        
        # 启动初始效果
        self.bg_fade_in.start()

        self.current_img=0



   # def dialog(self,screen):

        #音效控制
        # “effectDialog”音效：在每次说话人切换到bug时播放一次
        #if self.textNum != self.last_played_textNum and self.gameMode == 1:
            #if self.dialogNum == 1 and self.textNum in [1,3]:
                #self.effectDialog.play()
            #self.last_played_textNum = self.textNum






    def handle_mouse_button_down(self, event):

        print(self.gameMode,self.dialogNum)

        if self.gameMode == 1 and event.button == 1:
            if self.waiting_for_click:
                self.waiting_for_click = False
                # 根据当前状态决定下一步
                if self.transition_state == "bg_displayed":
                    self.transition_state = "bg_fade_out"
                    self.bg_fade_out.start()
                elif self.transition_state == "bgside_displayed":
                    # 这里可以添加其他逻辑
                    pass
                    
            if self.dialogNum in [1]:
                self.textNum += 1


        


        





    def update(self):
        super().update()
        
        # 更新当前活动的效果
        dt = 1.0 / 60.0  # 假设60FPS
        if self.transition_state == "bg_fade_in":
            self.bg_fade_in.update(dt)
            if self.bg_fade_in.is_finished():
                self.transition_state = "bg_displayed"
                self.waiting_for_click = True
                self.current_img=1
                
        elif self.transition_state == "bg_fade_out":
            self.current_img=0
            self.bg_fade_out.update(dt)
            if self.bg_fade_out.is_finished():
                self.transition_state = "bgside_fade_in"
                self.bgside_fade_in.start()
                
        elif self.transition_state == "bgside_fade_in":
            self.bgside_fade_in.update(dt)
            if self.bgside_fade_in.is_finished():
                self.transition_state = "bgside_displayed"
                self.waiting_for_click = True
                self.current_img=2

        

        if self.gameMode==1:

            if self.textNum >= 4 and self.dialogNum == 1:
                print("dialog1 over")
                self.textNum = 0
                self.dialogNum = 2
                self.is_level_end=True
                config.current_state = GameState.LEVEL15




    def draw(self):
        self.screen.fill((0, 0, 0))

        if self.current_img==1:
            self.screen.blit(self.bg, (0, 0))
        elif self.current_img==2:
            self.screen.blit(self.bgside, (0, 0))

        
        # 根据当前状态绘制图像
        if self.transition_state in ["bg_fade_in", "bg_displayed", "bg_fade_out"]:
            self.bg_fade_in.draw(self.screen)  # 这些类会自动处理绘制与否
            self.bg_fade_out.draw(self.screen)
        
        if self.transition_state in ["bgside_fade_in", "bgside_displayed"]:
            self.bgside_fade_in.draw(self.screen)




        x, y = pygame.mouse.get_pos()
        self.screen.blit(self.mouse, (x - 4, y - 4))


        if config.current_state == GameState.LEVEL15:  # 防止过渡完成后原场景会闪现一下
            self.screen.fill((0, 0, 0))


