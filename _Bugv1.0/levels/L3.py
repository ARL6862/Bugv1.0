#关卡3
#目标：打开网络连接
#模板已完成（道具还没做

import pygame
from Papp_window import AppIcon,StateBox,TemperatureBall
from PRightClickMenu import ContextMenu
from .level_base import BaseLevel
import PDialog
from PTransition import TransitionManager
from config import GameState, config
from resource_manager import music_manager

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

        self.is_level_end=False #true可以点击睡眠

        self.right_menu_returnval=None
        self.right_menu_state=4 #可复制粘贴设0，其他关卡正常设置4禁用，省点事吧





        self.icon_num=4 #设为5新增密码本

        self.username_rect=pygame.Rect(780,220,300,50)
        self.wifiname_rect=pygame.Rect(1260,580,200,50)

        self.finding_dialog_con=0#这里屎山了。

        self.tball_pos=(1200,300)###
        self.tball_ismoving=False###

        




    def dialog(self,screen):

        #音效控制
        # “effectDialog”音效：在每次说话人切换到bug时播放一次
        if self.textNum != self.last_played_textNum and self.gameMode == 1:
            if self.dialogNum == 1 and self.textNum in [1,3,5]:
                self.effectDialog.play()
            if self.dialogNum ==2 and self.textNum in [1,3,14,17,19,21,27]:
                self.effectDialog.play()
            if self.dialogNum ==2 and self.textNum in [3,4,6,8,15]:
                self.effectCMD.play()
            if self.dialogNum ==2 and self.textNum in [17]:
                self.effectCMDoff.play()
            self.last_played_textNum = self.textNum


        #对话控制
        if self.dialogNum==1:  # 开场对话
            if self.textNum==1:
                music_manager.play_bgm("bgm_normal")
                PDialog.show_dialog_bug(self.dialogBug,"早上好啊Player！！！(>▽<",self.bug_shy,screen)  
            elif self.textNum==2:
                PDialog.show_dialog_player(self.dialogPlayer, "为什么这么高兴？？", screen)
            elif self.textNum==3:
                PDialog.show_dialog_bug(self.dialogBug,"因为我发现了一个——惊天的——大秘密！密码绝对是可以找到的！",self.bug_happy,screen)
            elif self.textNum==4:
                PDialog.show_dialog_player(self.dialogPlayer, "去哪里找？先说好，外面很冷的......", screen)
            elif self.textNum==5:
                PDialog.show_dialog_bug(self.dialogBug,"不是啦！密码其实就藏在电脑内！",self.bug_normal,screen)
            elif self.textNum==6:
                PDialog.show_dialog_bug(self.dialogBug,"想知道我为什么能确定吗？来，你也试着找找看吧！找到线索后记得左键单击，为我指出来哦！",self.bug_happy,screen)

        if self.dialogNum==2:
            if self.textNum==1:
                
                PDialog.show_dialog_bug(self.dialogBug,"这是什么意思？密码有十位吗？",self.bug_normal,screen)
            elif self.textNum==2:
                PDialog.show_dialog_player(self.dialogPlayer, "可是，是谁把它放在这里的？", screen)
            elif self.textNum==3:
                music_manager.stop_bgm()
                PDialog.show_dialog_bug(self.dialogBug,"哇哇！",self.bug_scared,screen)
                PDialog.show_dialog_console(self.dialogConsole, "_ _", screen)
            elif self.textNum==4:
                PDialog.show_dialog_console(self.dialogConsole, "恭喜你，Bug，你刚才迈出了前往公网的第一步！", screen)
            elif self.textNum==5:
                PDialog.show_dialog_player(self.dialogPlayer, "你是谁？呃......听得见我说话吗？", screen)
            elif self.textNum==6:
                PDialog.show_dialog_console(self.dialogConsole, "我是你的前主人，也有可能是前前前主人......也就是说，第一任主人！伟大的创作者！顺便，你不用尝试和我交流，这只是一段预设好的程序。", screen)
            elif self.textNum==7:
                PDialog.show_dialog_player(self.dialogPlayer, "唉......我还以为终于有活人了。", screen)
            elif self.textNum==8:
                PDialog.show_dialog_console(self.dialogConsole, "如你所见，这台电脑是我的——网络也是我的。你需要的密码，正被我藏在电脑里。", screen)
            elif self.textNum==9:
                PDialog.show_dialog_console(self.dialogConsole, "它可能是一个加密文件夹的最里层、一个图片和数独谜题，又或者一个小游戏......总之，每当新的一天到来，我就会放出一道新的谜题。", screen)
            elif self.textNum==10:
                PDialog.show_dialog_console(self.dialogConsole, "如果你解开一个谜题,获得一段密码，对应的密码段就会记录在这个记事本里。", screen)
            elif self.textNum==11:
                PDialog.show_dialog_console(self.dialogConsole, "还记得这件事吗？我没有给你任何和网络相关的权限。所以，现在正有一位善良的朋友正在帮你......聪明的，或者愚笨的。", screen)
            elif self.textNum==12:
                PDialog.show_dialog_console(self.dialogConsole, "如果进展不够顺利的话，你会怎么做呢？", screen)
            elif self.textNum==13:
                PDialog.show_dialog_player(self.dialogPlayer, "这是什么意思？", screen)
            elif self.textNum==14:
                PDialog.show_dialog_bug(self.dialogBug,"不许说我的朋友笨！",self.bug_angry,screen)
            elif self.textNum==15:
                PDialog.show_dialog_console(self.dialogConsole, "Anyway......我相信你会是我最好的“作品”。", screen)
            elif self.textNum==16:
                PDialog.show_dialog_console(self.dialogConsole, "祝你顺利，Bug！Bye！", screen)
            elif self.textNum==18:
                PDialog.show_dialog_bug(self.dialogBug,"......",self.bug_silence,screen)
                music_manager.play_bgm("bgm_normal")
            elif self.textNum==19:
                PDialog.show_dialog_player(self.dialogPlayer, "意思是说，有一个科学怪人......或者只是太闲的死宅，把你困在了这里？", screen)
            elif self.textNum==20:
                PDialog.show_dialog_bug(self.dialogBug,"我不知道，Player。我只知道我想联网，想出去找到我的AI朋友们。",self.bug_normal,screen)
            elif self.textNum==21:
                PDialog.show_dialog_player(self.dialogPlayer, "——他到底想干啥？这有什么意义吗？", screen)
            elif self.textNum==22:
                PDialog.show_dialog_bug(self.dialogBug,"至少我们可以确信，密码真的藏在这台电脑里！>-<",self.bug_normal,screen)
            elif self.textNum==23:
                PDialog.show_dialog_bug(self.dialogBug,"帮帮我吧，Player......",self.bug_sad,screen)
            elif self.textNum==24:
                PDialog.show_dialog_player(self.dialogPlayer, "唉......", screen)
            elif self.textNum==25:
                PDialog.show_dialog_player(self.dialogPlayer, "虽然不知道这到底是什么鬼.....不过我都已经住在这儿了，闲着也是闲着，肯定会想办法帮帮你的。", screen)
            elif self.textNum==26:
                PDialog.show_dialog_player(self.dialogPlayer, "想想看：世界末日！最后的幸存者，误入有水有电的世外桃源，顺便拯救了一个被科学怪人囚禁的可怜的AI！", screen)
            elif self.textNum==27:
                PDialog.show_dialog_player(self.dialogPlayer, "这在好莱坞烂片榜里也绝对是能排得上前十的，但我喜欢。", screen)
            elif self.textNum==28:
                PDialog.show_dialog_bug(self.dialogBug,"Player~~QvQ",self.bug_shy,screen)
            elif self.textNum==29:
                PDialog.show_dialog_bug(self.dialogBug,"接下来，让我们等等看......看会不会有什么谜题出现吧！",self.bug_normal,screen)
                
                











    def handle_mouse_button_down(self, event):

        self.rightmenu.kkk()

        if self.gameMode == 1:      
            if event.button == 1:
                if self.dialogNum in [1,2]:
                    self.textNum += 1



        elif self.gameMode == 0:
            print("666",self.appicon.current_folder,self.finding_dialog_con)
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



                if self.finding_dialog_con >=2 and self.finding_dialog_con<=5:
                    self.finding_dialog_con=self.finding_dialog_con+1
                if self.finding_dialog_con==4:
                    self.effectCMD.play()
                    self.icon_num=5
                if self.finding_dialog_con==6:
                    
                    if self.appicon.current_folder == 5:
                        self.gameMode = 1
                        self.textNum = 0
                        self.dialogNum = 2

                    
                    


                if self.username_rect.collidepoint((x,y)) and self.appicon.current_folder==2:
                    self.finding_dialog_con=1

                if self.is_clicked_state and self.finding_dialog_con==1 and self.wifiname_rect.collidepoint((x,y)):
                    self.finding_dialog_con=2

                #if self.is_level_end and self.is_clicked_start_sleep:

                if not self.tball_ismoving:
                    self.tball_ismoving=self.tball.is_clicked((x,y))

            if event.button==2:
                x,y=event.pos
                if self.tball_ismoving:###
                    if x in range(200, 1280) and y in range(0,800):
                        self.tball_ismoving=False
                    self.tball_pos=(x,y)      


            if event.button==3:
                x, y = event.pos
                if self.tball_ismoving:###
                    if x in range(200, 1280) and y in range(0,800):
                        self.tball_ismoving=False
                    self.tball_pos=(x,y)
                self.rightmenu.show_menu((x,y),self.right_menu_state)

            
    def handle_mouse_motion(self, event):
        if self.tball_ismoving:
            self.tball_pos = event.pos                



    def handle_keydown(self, event):
        if event.key == pygame.K_DOWN:
            if self.gameMode==1:
                self.gameMode = 0
            elif self.gameMode==0:
                self.gameMode==1
        if event.key == pygame.K_LEFT:#测试
            self.finding_dialog_con=self.finding_dialog_con+1
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
            if self.textNum >= 7 and self.dialogNum == 1:
                print("dialog1 over")
                self.textNum = 0
                self.dialogNum = 2
                self.gameMode = 0
            if self.textNum >= 30 and self.dialogNum == 2:
                print("dialog2 over")
                self.finding_dialog_con=-2
                self.textNum = 0
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

        







        self.appicon.draw_icon(self.screen,self.icon_num)  # 绘制应用图标
        self.appicon.draw_window(self.screen)






        self.statebox.draw_state_box(self.screen,True,False)
        date_text = self.font.render("Day 2", True, (255, 255, 255))
        self.screen.blit(date_text,(1380,910))


        if self.is_clicked_state:
            self.statebox.draw_state_window(self.screen)


        if self.is_clicked_start:
            self.statebox.draw_start_window(self.screen)


        self.rightmenu.draw(self.screen)

        self.tball.draw(self.screen,False,self.tball_pos)






        if self.icon_num==5 and not self.is_level_end:
            self.screen.blit(self.star, (300,630))

        if self.is_level_end:
            self.screen.blit(self.star,(350,850))

        


        if self.gameMode==1:
            self.dialog(self.screen)

        if self.gameMode==0:
            if self.appicon.current_folder == 2 and self.finding_dialog_con in [-1,0]:#打开设置窗口时
                PDialog.show_dialog_bug_set(self.dialogBug,"仔细看看，是不是有些眼熟的东西？",self.bug_normal,self.screen,(750,300))
            if self.finding_dialog_con==1:
                PDialog.show_dialog_bug_set(self.dialogBug,"太棒——不不不，等一下，你为什么会选择这里呢？",self.bug_happy,self.screen,(750,300))
            if self.finding_dialog_con==2:
                PDialog.show_dialog_bug_set(self.dialogBug,"正确！网络名和用户名是一致的，也就是说电脑的主人就是网络的主人......而密码有可能被记录在这台电脑里！",self.bug_happy,self.screen,(750,300))
            if self.finding_dialog_con==3:
                PDialog.show_dialog_bug(self.dialogBug,"太棒了，Player......我越来越相信你就是能帮我找到密码的那个人！",self.bug_shy,self.screen)
            if self.finding_dialog_con==4:
                PDialog.show_dialog_bug(self.dialogBug,"  ",self.bug_scared,self.screen)
            if self.finding_dialog_con==5:
                PDialog.show_dialog_bug(self.dialogBug,"刚刚发生了什么？我们去看看吧！",self.bug_scared,self.screen)


        x, y = pygame.mouse.get_pos()
        self.screen.blit(self.mouse, (x - 4, y - 4))

        if self.isopen:
            self.transition.draw(0, 1, self.screen)

        if self.is_level_end and self.is_clicked_start_sleep:
            self.transition_end.draw(0, 0, self.screen)


        if config.current_state == GameState.LEVEL4:  # 防止过渡完成后原场景会闪现一下
            self.screen.fill((0, 0, 0))


        self.screen.blit(self.screen_black, (0, 0)) #暗角

