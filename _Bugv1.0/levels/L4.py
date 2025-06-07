#关卡2
#目标：打开网络连接


import pygame
from Papp_window import AppIcon
from .level_base import BaseLevel
import PDialog
from PTransition import TransitionManager

class Level4(BaseLevel):
    def __init__(self, screen, res_mgr):
        super().__init__(screen, res_mgr)
        self.bg = res_mgr.get_image("bg_normal")
        self.bgside = res_mgr.get_image("bgside_normal")

        self.bug_normal= res_mgr.get_image("bug_normal")
        self.bug_happy= res_mgr.get_image("bug_happy")
        self.bug_sad= res_mgr.get_image("bug_sad")
        self.bug_shy= res_mgr.get_image("bug_shy")
        self.bug_silence= res_mgr.get_image("bug_silence")
        self.bug_angry=res_mgr.get_image("bug_angry")


        self.mouse=res_mgr.get_image("mouse_normal")

        self.dialogPlayer=res_mgr.get_image("dialog_player")
        self.dialogBug=res_mgr.get_image("dialog_bug")

        self.screen_black = res_mgr.get_image("screen_black")

        self.font = res_mgr.load_font("default", size=48)

        self.effectDialog=res_mgr.get_sound("effect_dialog")

        #对话控制相关参数
        self.textNum=0#当前对话段的文本序号（例如①bug：111 ②Player：222 ③bug：333...）
        self.dialogNum=1#对话段序号（例如段①：游戏开始时；段②：新手教程时；段③：游戏结束时）
        self.gameMode = 0   #0=normal;1=dialog，用这个变量来控制当前是游戏模式or剧情模式（玩家不可进行鼠标点击推进对话外的操作，bug也不会乱跑）
        self.last_played_textNum = -1  # 记录上一次播放音效的文本编号，用来控制音效免得在循环中反复播放


        self.transition = TransitionManager(1680, 960)
        self.isopen=True #开场过渡
        self.transition_over=False

        self.appicon = AppIcon()  # 创建AppIcon实例



    def dialog(self,screen):

        #音效控制
        # “effectDialog”音效：在每次说话人切换到bug时播放一次
        """ if self.textNum != self.last_played_textNum and self.gameMode == 1:
            if self.dialogNum == 1 and self.textNum in [1,5, 8]:
                self.effectDialog.play()
            elif self.dialogNum == 2 and self.textNum in [1,9,11,14,17,19,21,24,30,33]:
                self.effectDialog.play()
            self.last_played_textNum = self.textNum """


        #对话控制
        if self.dialogNum==1:#开场
            if self.textNum==1:
                PDialog.show_dialog_bug(self.dialogBug,"嗨! :)",self.bug_happy,screen)   #bug说话时 show_dialog_bug（对话框图片，文本，bug立绘）
            """ elif self.textNum==2:
                PDialog.show_dialog_bug(self.dialogBug,"你好，我是Bug！",self.bug_normal,screen)
            elif self.textNum==3:
                PDialog.show_dialog_bug(self.dialogBug,"如你所见，我是一个AI，被困在这个地下庇护所的旧电脑里。",self.bug_normal,screen)
            elif self.textNum==4:
                PDialog.show_dialog_player(self.dialogPlayer, "AI?", screen)   #player说话时 show_dialog_player（对话框图片，文本） """

            
                










    def handle_mouse_button_down(self, event):

        if event.button == 1:
            if self.gameMode == 1:
                self.textNum += 1


            elif self.gameMode == 0:
                x, y = event.pos
                if self.appicon.is_clicked((x, y)):
                    id= self.appicon.is_clicked((x, y))
                    if self.appicon.selected_icon :
                        self.appicon.display_window = id
                        self.appicon.selected_icon = None
                    else:
                        self.appicon.selected_icon = id 
                        print(id,"App icon clicked!")
                
                pygame.display.flip()





    def handle_keydown(self, event):# 测试用
        if event.key == pygame.K_DOWN:
            self.gameMode = 0



    def update(self):
        super().update()
        self.transition_over=self.transition.update()
        if self.isopen and not self.transition.is_active():
                self.transition.start(duration=500)
        if self.transition_over:
            self.isopen=False
            self.transition_over=False


        """ if self.textNum >= 9 and self.dialogNum == 1:
            print("dialog1 over")
            self.textNum = 0
            self.dialogNum = 2 """


            



    def draw(self):

 
        self.screen.blit(self.bgside, (0, 0))
        self.screen.blit(self.bg, (200, 0))



        
        if self.gameMode==1:
            self.dialog(self.screen)


        x, y = pygame.mouse.get_pos()
        self.screen.blit(self.mouse, (x - 4, y - 4))

        self.appicon.draw_icon(self.screen)  # 绘制应用图标
        self.appicon.draw_window(self.screen)

        if self.isopen:
            self.transition.draw(0, 1, self.screen)


        self.screen.blit(self.screen_black, (0, 0))


        text = self.font.render("level4", True, (255,255,255))
        self.screen.blit(text, (20,20)) 

