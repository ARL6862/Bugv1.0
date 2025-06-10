#关卡3
#目标：打开网络连接
#模板已完成

import pygame
from Papp_window import AppIcon,StateBox,TemperatureBall
from PRightClickMenu import ContextMenu
from .level_base import BaseLevel
import PDialog
from PTransition import TransitionManager
from config import GameState, config

class Level3(BaseLevel):
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
        self.bug_scared=res_mgr.get_image("bug_scared")


        self.mouse=res_mgr.get_image("mouse_normal")

        self.dialogPlayer=res_mgr.get_image("dialog_player")
        self.dialogBug=res_mgr.get_image("dialog_bug")

        self.screen_black = res_mgr.get_image("screen_black")

        self.font = res_mgr.load_font("default", size=48)

        self.effectDialog=res_mgr.get_sound("effect_dialog")

        #对话控制相关参数
        self.textNum=0#当前对话段的文本序号（例如①bug：111 ②Player：222 ③bug：333...）
        self.dialogNum=1#对话段序号（例如段①：游戏开始时；段②：新手教程时；段③：游戏结束时）
        self.gameMode = 1   #0=normal;1=dialog，用这个变量来控制当前是游戏模式or剧情模式（玩家不可进行鼠标点击推进对话外的操作，bug也不会乱跑）
        self.last_played_textNum = -1  # 记录上一次播放音效的文本编号，用来控制音效免得在循环中反复播放


        self.transition = TransitionManager(1680, 960)
        self.isopen=True #开场过渡
        self.transition_over=False

        self.transition_end = TransitionManager(1680, 960)
        self.isend=False #结束过渡
        self.transition_end_over=False


        self.is_clicked_start=False
        self.is_clicked_start_sleep=False #true前往下一关
        self.is_clicked_state=False


        self.appicon = AppIcon()  # 创建应用图标与窗口管理实例
        self.statebox=StateBox()  #创建状态栏控制实例
        self.tball=TemperatureBall() #创建温度球
        self.rightmenu=ContextMenu(self.screen,0) #创建右键菜单栏

        self.font_small=res_mgr.load_font("small", size=20)

        self.is_level_end=False #true时开始进行过渡，过渡完到下一关

        self.right_menu_returnval=None
        self.right_menu_state=4 #可复制粘贴设0，其他关卡正常设置4禁用，省点事吧




    def dialog(self,screen):

        #音效控制
        # “effectDialog”音效：在每次说话人切换到bug时播放一次
        if self.textNum != self.last_played_textNum and self.gameMode == 1:
            if self.dialogNum == 1 and self.textNum in [1]:
                self.effectDialog.play()
            self.last_played_textNum = self.textNum


        #对话控制
        if self.dialogNum==1:#开场
            if self.textNum==1:
                PDialog.show_dialog_bug(self.dialogBug,"嗨! :)",self.bug_happy,screen)   #bug说话时 show_dialog_bug（对话框图片，文本，bug立绘）
            elif self.textNum==2:
                PDialog.show_dialog_bug(self.dialogBug,"你好，我是Bug！",self.bug_normal,screen)
            elif self.textNum==3:
                PDialog.show_dialog_bug(self.dialogBug,"如你所见，我是一个AI，被困在这个地下庇护所的旧电脑里。",self.bug_normal,screen)
            elif self.textNum==4:
                PDialog.show_dialog_player(self.dialogPlayer, "AI?", screen)   #player说话时 show_dialog_player（对话框图片，文本）











    def handle_mouse_button_down(self, event):

        self.rightmenu.kkk()

        if self.gameMode == 1:      
            if event.button == 1:
                if self.dialogNum == 1:
                    self.textNum += 1



        elif self.gameMode == 0:
            x, y = event.pos

            if event.button == 1:
                id= self.appicon.is_clicked((x, y))
                if id is not None:
                    if self.appicon.selected_icon :
                        self.appicon.display_window = id
                        self.appicon.selected_icon = None
                    else:
                        self.appicon.selected_icon = id 

                self.appicon.is_button_clicked((x,y))
                self.is_clicked_state=self.statebox.is_clicked_state((x,y))
                self.is_clicked_start=self.statebox.is_clicked_start((x,y))



                if self.is_clicked_start:
                    self.is_clicked_start_sleep = self.statebox.is_clicked_start_sleep((x,y), self.is_level_end)
                    if self.is_clicked_start_sleep:
                        print("准备切换到下一关")




                if self.rightmenu.handle_left_click((x,y),self.right_menu_state):
                    self.right_menu_returnval=self.rightmenu.get_return_value()
                    if self.right_menu_returnval==0:
                        self.right_menu_state=1
                    elif self.right_menu_returnval==1 or self.right_menu_returnval==None:
                        self.right_menu_state=0
                    elif self.right_menu_returnval==5:
                        print("当前关卡禁用复制粘贴")

                


            if event.button==3:
                self.rightmenu.show_menu((x,y),self.right_menu_state)

            
                



    def handle_keydown(self, event):
        if event.key == pygame.K_DOWN:
            if self.gameMode==1:
                self.gameMode = 0
            elif self.gameMode==0:
                self.gameMode==1
        if event.key==pygame.K_r:
            self.appicon.reset()
            print("reset!!!")





    def update(self):
        super().update()
        
        self.transition_over=self.transition.update()
        if self.isopen and not self.transition.is_active():
                self.transition.start(duration=500)


        if self.gameMode==1:
            if self.transition_over:
                self.isopen=False
                self.transition_over=False
            if self.textNum >= 5 and self.dialogNum == 1:
                print("dialog1 over")
                self.textNum = 0
                #self.dialogNum = 2


                self.dialogNum = 0
                self.gameMode = 0
                self.is_level_end=True


        elif self.gameMode==0:
            self.transition_end_over = self.transition_end.update()
            if self.is_level_end and self.is_clicked_start_sleep:
                if not self.transition_end.is_active():
                    self.transition_end.start(duration=2000,text="Day 2    --->    Day 3")

                # 过渡完成后切换关卡
                if self.transition_end_over:
                    config.current_state = GameState.LEVEL4
                    self.transition_end_over = False

            


            



    def draw(self):

 
        self.screen.blit(self.bgside, (0, 0))
        self.screen.blit(self.bg, (200, 0))

        







        self.appicon.draw_icon(self.screen)  # 绘制应用图标
        self.appicon.draw_window(self.screen)






        self.statebox.draw_state_box(self.screen,True,False)

        if self.is_clicked_state:
            self.statebox.draw_state_window(self.screen)


        if self.is_clicked_start:
            self.statebox.draw_start_window(self.screen)




        self.tball.draw(self.screen,False)


        self.rightmenu.draw(self.screen)








        if self.gameMode==1:
            self.dialog(self.screen)


        x, y = pygame.mouse.get_pos()
        self.screen.blit(self.mouse, (x - 4, y - 4))

        if self.isopen:
            self.transition.draw(0, 1, self.screen)

        if self.is_level_end and self.is_clicked_start_sleep:
            self.transition_end.draw(0, 0, self.screen)


        if config.current_state == GameState.LEVEL4:  # 防止过渡完成后原场景会闪现一下
            self.screen.fill((0, 0, 0))


        self.screen.blit(self.screen_black, (0, 0)) #暗角

