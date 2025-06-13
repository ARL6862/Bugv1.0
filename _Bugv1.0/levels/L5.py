#目标：打开网络连接
#密码：6 （7）

import pygame
from Papp_window import AppIcon,StateBox,TemperatureBall,PasswordWindow
from PRightClickMenu import ContextMenu
from .level_base import BaseLevel
import PDialog
from PTransition import TransitionManager
from config import GameState, config
from resource_manager import music_manager

class Level5(BaseLevel):
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
        self.gameMode = 0   #0=normal;1=dialog，用这个变量来控制当前是游戏模式or剧情模式（玩家不可进行鼠标点击推进对话外的操作，bug也不会乱跑）
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

        self.is_password_win_display=False
        self.is_password_get=False

        self.is_dialog3_try=False####try
        self.is_dialog2_try=False


        self.niudun1=res_mgr.get_image("niudun1")
        self.niudun2=res_mgr.get_image("niudun2")
        self.niudun3=res_mgr.get_image("niudun3")
        self.apple=res_mgr.get_image("apple")


        self.niudun_rect=pygame.Rect(600,250,650,500)

        self.is_apple_moving=False
        self.is_niudun_addapple=False
        self.apple_pos=(0,0)

        self.niudun_addapple_wait = False
        self.niudun_addapple_start_time = 0
        self.niudun_addapple_current_time=0

        self.appicon.password_num=1
       






        




    def dialog(self,screen):

        #音效控制
        # “effectDialog”音效：在每次说话人切换到bug时播放一次
        if self.textNum != self.last_played_textNum and self.gameMode == 1:
            if self.dialogNum == 1 and self.textNum in [1,3]:
                self.effectDialog.play()
            self.last_played_textNum = self.textNum


        #对话控制
        if self.dialogNum==1:  # 打开图片后对话
            if self.textNum==1:
                music_manager.play_bgm("bgm_normal")
                PDialog.show_dialog_bug(self.dialogBug,"111",self.bug_shy,screen)  
            elif self.textNum==2:
                PDialog.show_dialog_player(self.dialogPlayer, "111", screen)
            elif self.textNum==3:
                PDialog.show_dialog_bug(self.dialogBug,"111",self.bug_happy,screen)

        if self.dialogNum==2:   #   捡起苹果后对话
            if self.textNum==1:
                music_manager.play_bgm("bgm_normal")
                PDialog.show_dialog_bug(self.dialogBug,"222",self.bug_shy,screen)  
            elif self.textNum==2:
                PDialog.show_dialog_player(self.dialogPlayer, "222", screen)
            elif self.textNum==3:
                PDialog.show_dialog_bug(self.dialogBug,"222",self.bug_happy,screen)

        if self.dialogNum==3:   #   谜题完成后对话
            if self.textNum==1:
                music_manager.play_bgm("bgm_normal")
                PDialog.show_dialog_bug(self.dialogBug,"333",self.bug_shy,screen)  
            elif self.textNum==2:
                PDialog.show_dialog_player(self.dialogPlayer, "333", screen)
            elif self.textNum==3:
                PDialog.show_dialog_bug(self.dialogBug,"333",self.bug_happy,screen)                
                

        if self.dialogNum==4:   #猜完密码    
            if self.textNum==1:
                PDialog.show_dialog_player(self.dialogPlayer, "简简单单！", screen)
            elif self.textNum==2:
                PDialog.show_dialog_bug(self.dialogBug, "幸好有你，Player。", self.bug_happy, screen)
            elif self.textNum==3:
                PDialog.show_dialog_bug(self.dialogBug, "不然牛顿都想不出来的问题，我一个楚楚可怜、弱不禁风、憨态可掬的AI，怎么会得出这样高深奥妙的答案？", self.bug_normal, screen)
            elif self.textNum==4:
                PDialog.show_dialog_bug(self.dialogBug, "我知道牛顿是一个虔诚的基督徒。“创作者”，你敢再出这么弱智又无聊的谜题，就去跟他一道去见上帝吧！！！", self.bug_angry, screen)
            elif self.textNum==5:
                PDialog.show_dialog_player(self.dialogPlayer, "现在是世界末日，他应该已经在上帝那儿了。", screen)
            elif self.textNum==6:
                PDialog.show_dialog_bug(self.dialogBug, "对哦。", self.bug_scared, screen)





    def handle_mouse_button_down(self, event):

        print(self.gameMode,self.dialogNum)

        if self.gameMode == 1:      
            if event.button == 1:
                if self.dialogNum in [1,2,3,4]:
                    self.textNum += 1



        elif self.gameMode == 0:
            
            x, y = event.pos

            self.apple_pos=event.pos


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




                if self.appicon.current_folder==6 and self.appicon.selected_icon==14:#apple
                    self.is_apple_moving=True




                if self.is_clicked_start:
                    self.is_clicked_start_sleep = self.statebox.is_clicked_start_sleep((x,y), self.is_level_end)
                    if self.is_clicked_start_sleep:
                        music_manager.stop_bgm()
                        self.effectChangeLevel.play()
                        print("准备切换到下一关")

                    
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

                if self.appicon.current_folder==15 and self.dialogNum==1:
                    self.gameMode=1
                if self.is_apple_moving and self.dialogNum==2:
                    self.gameMode=1
                if self.niudun_addapple_wait and self.dialogNum==3:
                    self.gameMode=1
                if  self.is_password_get and self.dialogNum==4:
                    self.appicon.password_num=2
                    self.gameMode=1


                


            if event.button==2:   
                x, y = event.pos
                if self.tball_ismoving:###
                    if x in range(200, 1280) and y in range(0,800):
                        self.tball_ismoving=False
                    self.tball_pos=(x,y)
                if self.niudun_rect.collidepoint(x, y) and self.appicon.current_folder==15:
                    self.is_niudun_addapple=True
                    self.niudun_addapple_start_time=pygame.time.get_ticks()
                self.is_apple_moving=False



            if event.button==3:
                x, y = event.pos

                                    
                self.rightmenu.show_menu((x,y),self.right_menu_state)


                

            
    def handle_mouse_motion(self, event):
        if self.tball_ismoving:
            self.tball_pos = event.pos   

        if self.is_apple_moving:
            self.apple_pos=event.pos             



    def handle_keydown(self, event):
        self.password_window.keydown(event)
        self.is_password_get=self.password_window.check_password(7)###############
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
        print("current floader",self.appicon.current_folder)

        if self.dialogNum==4 and self.gameMode==0:#密码框出现
            self.is_password_win_display=True


        if self.dialogNum==4 and self.gameMode==1:#密码本

            if self.textNum==2:
                self.is_password_win_display=False
                self.appicon.reset()
                self.appicon.current_folder=5 


        if self.is_niudun_addapple:
            self.niudun_addapple_current_time=pygame.time.get_ticks()
            if self.niudun_addapple_current_time-self.niudun_addapple_start_time>=1000:
                self.niudun_addapple_wait=True


        self.transition_over=self.transition.update()
        if self.isopen and not self.transition.is_active():
                self.transition.start(duration=500)


        if self.transition_over:#记得给它挪外边来不然开场不是剧情模式就老实了，好弱智的bug
                self.isopen=False
                self.transition_over=False


        if self.gameMode==1:
            
            if self.textNum >= 4 and self.dialogNum == 1:
                print("dialog1 over")
                self.textNum = 1
                self.dialogNum = 2
                self.gameMode = 0
                self.right_menu_state=0
            if self.textNum >= 4 and self.dialogNum == 2:
                print("dialog2 over")
                self.textNum = 1
                self.dialogNum = 3
                self.gameMode = 0
                self.right_menu_state=5
            if self.textNum >= 4 and self.dialogNum == 3:
                print("dialog3 over")
                self.textNum = 1
                self.dialogNum = 4
                self.gameMode = 0
            if self.textNum >= 7 and self.dialogNum == 4:
                print("dialog4 over")
                self.textNum = 1
                self.dialogNum = 0
                self.gameMode = 0
                self.is_level_end=True



        elif self.gameMode==0:
            self.transition_end_over = self.transition_end.update()
            if self.is_level_end and self.is_clicked_start_sleep:
                if not self.transition_end.is_active():
                    self.transition_end.start(duration=2000,text="Day 4    --->    Day 5")

                # 过渡完成后切换关卡
                if self.transition_end_over:
                    config.current_state = GameState.LEVEL6
                    self.transition_end_over = False

            


            



    def draw(self):

 
        self.screen.blit(self.bgside, (0, 0))
        self.screen.blit(self.bg, (200, 0))

        self.appicon.draw_icon(self.screen,15)  # 绘制应用图标
        self.appicon.draw_window(self.screen)########


        self.statebox.draw_state_box(self.screen,True,False)
        date_text = self.font.render("Day 4", True, (255, 255, 255))
        self.screen.blit(date_text,(1380,910))

        if self.appicon.current_folder==15:
            if self.niudun_addapple_wait:
                self.screen.blit(self.niudun3,(600,250))
            elif self.is_niudun_addapple:
                self.screen.blit(self.niudun2,(600,250))
            else:
                self.screen.blit(self.niudun1,(600,250))

        if self.is_apple_moving:
            self.screen.blit(self.apple,self.apple_pos)

        if self.is_clicked_state:
            self.statebox.draw_state_window(self.screen)


        if self.is_clicked_start:
            self.statebox.draw_start_window(self.screen)


        if self.is_password_win_display:
            self.password_window.draw(self.screen,(850,400),self.is_password_get)

        
        self.rightmenu.draw(self.screen)

        self.tball.draw(self.screen,False,self.tball_pos)


        if self.is_level_end:
            self.screen.blit(self.star,(350,850))


        if self.gameMode==1:
            self.dialog(self.screen)



        x, y = pygame.mouse.get_pos()
        self.screen.blit(self.mouse, (x - 4, y - 4))

        if self.isopen:
            self.transition.draw(0, 1, self.screen)

        if self.is_level_end and self.is_clicked_start_sleep:
            self.transition_end.draw(0, 0, self.screen)


        if config.current_state == GameState.LEVEL6:  # 防止过渡完成后原场景会闪现一下
            self.screen.fill((0, 0, 0))


        self.screen.blit(self.screen_black, (0, 0)) #暗角