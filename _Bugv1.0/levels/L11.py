#重启后 结局分支 假结局
#差文案音效 和真结局线假结局差分


#流程：报错弹窗-对话1-任务管理器结束错误进程-对话2+密码-更多报错弹窗-重启（关机）-分支
    #分支1（未发现真相）：-开机界面输入Password-开机-对话3-联网-对话4-bad ending
    #分支2（发现真相但未开启卸载程序）：-开机界面输入password-开机-对话5-分支   #-联网-对话4-bad ending
                                                                           #-拒绝联网（等待1分钟以上或进行关机/睡眠操作）-对话6-bad ending
    #分支3（发现真相且开启卸载程序）：-开机界面输入联网密码-开机-对话7+弹窗（卸载程序进度）-点击最终卸载确认-对话8 bug删除-桌面乱码（新增很多垃圾文件）-点击“实验日志”进入true ending

import random
import pygame
from Papp_window import AppIcon,StateBox,TemperatureBall,PasswordWindow
from PRightClickMenu import ContextMenu
from .level_base import BaseLevel
import PDialog
from PTransition import TransitionManager
from config import GameState, config
from resource_manager import music_manager,ending_manager

class Level11(BaseLevel):
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

        # 计时器变量
        self.timer_started = False
        self.timer_count = 0


        self.mouse=res_mgr.get_image("mouse_normal")

        self.dialogPlayer=res_mgr.get_image("dialog_player")
        self.dialogBug=res_mgr.get_image("dialog_bug")
        self.dialogConsole=res_mgr.get_image("dialog_cmd")

        self.screen_black = res_mgr.get_image("screen_black")

        self.star = res_mgr.get_image("star")

        self.font = res_mgr.load_font("default", size=48)

        self.effectDialog=res_mgr.get_sound("effect_dialog")
        self.effectCMD=res_mgr.get_sound("effect_cmd")
        self.effectCMDoff=res_mgr.get_sound("effect_cmdoff")
        self.effectChangeLevel=res_mgr.get_sound("effect_changelevel")

        #对话控制相关参数
        self.textNum=0#当前对话段的文本序号（例如①bug：111 ②Player：222 ③bug：333...）
        self.dialogNum=1#对话段序号（例如段①：游戏开始时；段②：新手教程时；段③：游戏结束时）
        self.gameMode = 1   #0=normal;1=dialog，用这个变量来控制当前是游戏模式or剧情模式（玩家不可进行鼠标点击推进对话外的操作，bug也不会乱跑）
        #4 开机界面
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
        self.password_window=PasswordWindow()

        self.font_small=res_mgr.load_font("small", size=20)

        self.is_level_end=False #true可以点击睡眠

        self.right_menu_returnval=None
        self.right_menu_state=4 #可复制粘贴设0，其他关卡正常设置4禁用，省点事吧

        self.tball_pos=(1200,300)###
        self.tball_ismoving=False###

        self.paste_area = pygame.Rect(500, 150, 780, 650)  

        self.is_password_txt_display=False  
        self.is_wifi_display=False
        self.is_password_win_display=False  #在这里充当联网密码输入
        self.is_password_get=False













        




    def dialog(self,screen):

        #音效控制
        # “effectDialog”音效：在每次说话人切换到bug时播放一次
        if self.textNum != self.last_played_textNum and self.gameMode == 1:
            if self.dialogNum == 1 and self.textNum in [1,3]:
                self.effectDialog.play()
            self.last_played_textNum = self.textNum


        #对话控制
        if self.dialogNum==1:  #开场
            if self.textNum==1:
                #music_manager.play_bgm("bgm_normal")
                PDialog.show_dialog_bug(self.dialogBug,"111",self.bug_shy,screen)  
            elif self.textNum==2:  #密码本显示 暂定
                self.is_password_txt_display=True
                self.appicon.current_folder=5
                PDialog.show_dialog_player(self.dialogPlayer, "111", screen)
            elif self.textNum==3:  #网络界面显示 暂定
                self.is_wifi_display=True
                self.is_clicked_state=True
                PDialog.show_dialog_bug(self.dialogBug,"111",self.bug_happy,screen)
            elif self.textNum==4:  #密码框显示 暂定
                self.is_password_win_display=True
                PDialog.show_dialog_bug(self.dialogBug,"111",self.bug_happy,screen)

               
            

        if self.dialogNum==2:   #   联网成功
            if self.textNum==1:
                #music_manager.play_bgm("bgm_normal")
                PDialog.show_dialog_bug(self.dialogBug,"222",self.bug_shy,screen)  
                self.is_password_win_display=False
            elif self.textNum==2:
                
                PDialog.show_dialog_player(self.dialogPlayer, "222", screen)
                
            elif self.textNum==3:
                PDialog.show_dialog_bug(self.dialogBug,"222",self.bug_happy,screen)

        if self.dialogNum==3:   #   2后等待5秒 预备boom
            if self.textNum==1:
                #music_manager.play_bgm("bgm_normal")
                PDialog.show_dialog_bug(self.dialogBug,"333",self.bug_shy,screen)  
            elif self.textNum==2:
                PDialog.show_dialog_player(self.dialogPlayer, "333", screen)
            elif self.textNum==3:
                PDialog.show_dialog_bug(self.dialogBug,"333",self.bug_happy,screen)                
                
 





    def handle_mouse_button_down(self, event):

        

        print(self.gameMode,self.dialogNum)

        if self.gameMode == 1:      
            if event.button == 1:
                if self.dialogNum in [1,2,3,4]:
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



                    

                    
                if self.rightmenu.handle_left_click((x,y),self.right_menu_state):
                    self.right_menu_returnval=self.rightmenu.get_return_value()
                    if self.right_menu_returnval==0:
                        self.right_menu_state=1
                    elif self.right_menu_returnval==1 or self.right_menu_returnval==None:
                        self.right_menu_state=0
                    elif self.right_menu_returnval==5:
                        print("当前关卡禁用复制粘贴")

                if not self.tball_ismoving:
                    self.tball_ismoving=self.tball.is_clicked((x,y))###



            if event.button==2:
                x,y=event.pos
                if self.tball_ismoving:###
                    if x in range(200, 1280) and y in range(0,800):
                        self.tball_ismoving=False
                    self.tball_pos=(x,y)       


            if event.button==3:
                x, y = event.pos


                self.rightmenu.show_menu((x,y),self.right_menu_state)
                

            
    def handle_mouse_motion(self, event):
        if self.tball_ismoving:
            self.tball_pos = event.pos                



    def handle_keydown(self, event):
        self.password_window.keydown(event)
        self.is_password_get=self.password_window.check_password(123456)###############联网密码
        if self.is_password_get:
            self.gameMode=1
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

        if self.transition_over:
                self.isopen=False
                self.transition_over=False


        if self.gameMode==1:
            
            if self.textNum >= 5 and self.dialogNum == 1:
                print("dialog1 over")
                self.textNum = 0
                self.dialogNum = 2
                self.gameMode = 0
            if self.textNum >= 4 and self.dialogNum == 2:
                print("dialog2 over")
                self.textNum = 0
                self.dialogNum = 3
                self.gameMode = 0

            if self.textNum >= 4 and self.dialogNum == 3:
                print("dialog3 over")
                self.textNum = 0
                self.dialogNum = 4
                self.gameMode = 0
                self.is_level_end=True




        elif self.gameMode==0:
            # 检查是否满足计时条件
            if self.dialogNum == 3 and self.textNum == 0 and not self.timer_started:
                self.timer_started = True
                self.timer_count = 0
            
            # 计时逻辑
            if self.timer_started:
                self.timer_count += 1/60  # 假设60fps
                if self.timer_count >= 5:  # 5秒后
                    self.gameMode = 1
                    self.timer_started = False

            self.transition_end_over = self.transition_end.update()
            if self.is_level_end and self.is_clicked_start_sleep:
                if not self.transition_end.is_active():
                    self.transition_end.start(duration=2000,text="BOOM!!")

                # 过渡完成后切换关卡
                if self.transition_end_over:
                    config.current_state = GameState.LEVEL13
                    self.transition_end_over = False

            


            



    def draw(self):

 
        self.screen.blit(self.bgside, (0, 0))
        self.screen.blit(self.bg, (200, 0))

        self.appicon.draw_icon(self.screen,25)  # 绘制应用图标  




        self.appicon.draw_window(self.screen)

        

        if self.is_password_get:
            self.statebox.draw_state_box(self.screen,True,True)
        else:
            self.statebox.draw_state_box(self.screen,True,False)


        date_text = self.font.render("Day 8", True, (255, 255, 255))
        self.screen.blit(date_text,(1380,910))

        if self.is_clicked_state:
            self.statebox.draw_state_window(self.screen)


        if self.is_clicked_start:
            self.statebox.draw_start_window(self.screen)


        if self.is_password_win_display:
            self.password_window.draw(self.screen,(850,400),self.is_password_get)

        
        self.rightmenu.draw(self.screen)

        self.tball.draw(self.screen,False,self.tball_pos)


        


        if self.gameMode==1:
            self.dialog(self.screen)





        x, y = pygame.mouse.get_pos()
        self.screen.blit(self.mouse, (x - 4, y - 4))

        if self.isopen:
            self.transition.draw(0, 1, self.screen)

        if self.is_level_end and self.is_clicked_start_sleep:
            self.transition_end.draw(0, 0, self.screen)


        if config.current_state == GameState.LEVEL13:  # 防止过渡完成后原场景会闪现一下
            self.screen.fill((0, 0, 0))


        self.screen.blit(self.screen_black, (0, 0)) #暗角