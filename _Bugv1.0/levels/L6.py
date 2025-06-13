#目标：接球
#密码：6 7 （1 2）

import pygame
import random
from Papp_window import AppIcon,StateBox,TemperatureBall,PasswordWindow
from PRightClickMenu import ContextMenu
from .level_base import BaseLevel
import PDialog
from PTransition import TransitionManager
from config import GameState, config
from resource_manager import music_manager

class Level6(BaseLevel):
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
        self.game_font = res_mgr.load_font("default", size=36)  # 接球游戏字体

        self.effectDialog=res_mgr.get_sound("effect_dialog")
        self.effectCMD=res_mgr.get_sound("effect_cmd")
        self.effectCMDoff=res_mgr.get_sound("effect_cmdoff")
        self.effectChangeLevel=res_mgr.get_sound("effect_changelevel")

        #对话控制相关参数
        self.textNum=0
        self.dialogNum=1
        self.gameMode = 1   #0=normal;1=dialog;2=catch_game
        self.last_played_textNum = -1

        self.transition = TransitionManager(1680, 960)
        self.isopen=True
        self.transition_over=False

        self.transition_end = TransitionManager(1680, 960)
        self.isend=False
        self.transition_end_over=False

        self.is_clicked_start=False
        self.is_clicked_start_sleep=False
        self.is_clicked_state=False

        self.appicon = AppIcon()
        self.statebox=StateBox()
        self.tball=TemperatureBall()
        self.rightmenu=ContextMenu(self.screen,0)
        self.password_window=PasswordWindow()

        self.font_small=res_mgr.load_font("small", size=20)

        self.is_level_end=False

        self.right_menu_returnval=None
        self.right_menu_state=4

        self.tball_pos=(1200,300)
        self.tball_ismoving=False

        self.paste_area = pygame.Rect(500, 150, 780, 650)

        self.is_password_win_display=False
        self.is_password_get=False

        self.is_dialog3_try=False
        self.is_dialog2_try=False

        # 接球游戏参数
        self.game_area_left = 500
        self.game_area_top = 150
        self.game_area_right = 1300
        self.game_area_bottom = 750
        self.game_area_width = self.game_area_right - self.game_area_left
        self.game_area_height = self.game_area_bottom - self.game_area_top
        
        self.reset_catch_game()
        self.paddle_speed = 10
        self.ball_speed_increase = 0.5




    def reset_catch_game(self):
        
        self.paddle_width = 100
        self.paddle_height = 20
        self.paddle_x = self.game_area_left + (self.game_area_width - self.paddle_width) // 2
        self.paddle_y = self.game_area_bottom - 40
        
        self.ball_radius = 10
        self.ball_x = self.game_area_left + self.game_area_width // 2
        self.ball_y = self.game_area_top + self.game_area_height // 2
        self.ball_dx = 5 * random.choice([-1, 1])
        self.ball_dy = -5
        
        self.catch_score = 0
        self.catch_game_over = False
        self.catch_game_won = False




    def update_catch_game(self):
        
        if not self.catch_game_over and not self.catch_game_won:
            # 使用A/D键控制平板
            if self.keys_pressed[pygame.K_a] and self.paddle_x > self.game_area_left:
                self.paddle_x -= self.paddle_speed
            if self.keys_pressed[pygame.K_d] and self.paddle_x < self.game_area_right - self.paddle_width:
                self.paddle_x += self.paddle_speed
            
            # 更新小球位置
            self.ball_x += self.ball_dx
            self.ball_y += self.ball_dy
            
            # 墙壁碰撞 - 限制在游戏区域内
            if (self.ball_x <= self.game_area_left + self.ball_radius or 
                self.ball_x >= self.game_area_right - self.ball_radius):
                self.ball_dx *= -1
            if self.ball_y <= self.game_area_top + self.ball_radius:
                self.ball_dy *= -1
            
            # 平板碰撞
            if (self.ball_y + self.ball_radius >= self.paddle_y and 
                self.paddle_x <= self.ball_x <= self.paddle_x + self.paddle_width and 
                self.ball_dy > 0):
                
                self.ball_dy *= -1
                self.catch_score += 1
                
                # 每反弹一次增加速度
                if self.ball_dx > 0:
                    self.ball_dx += self.ball_speed_increase
                else:
                    self.ball_dx -= self.ball_speed_increase
                self.ball_dy -= self.ball_speed_increase
                
                # 胜利条件：十二次连击
                if self.catch_score >= 12:
                    self.catch_game_won = True
            
            # 掉落检测
            if self.ball_y >= self.game_area_bottom + self.ball_radius:
                self.catch_game_over = True




    def draw_catch_game(self):
        # 绘制游戏区域边界
        pygame.draw.rect(self.screen, (0, 0, 0), 
                        (self.game_area_left, self.game_area_top, 
                         self.game_area_width, self.game_area_height))
        
        
        # 绘制平板和小球
        pygame.draw.rect(self.screen, (255, 255, 255), 
                         (self.paddle_x, self.paddle_y, self.paddle_width, self.paddle_height))
        pygame.draw.circle(self.screen, (255, 255, 255), 
                          (int(self.ball_x), int(self.ball_y)), self.ball_radius)
        
        pygame.draw.rect(self.screen, (100, 0, 80), 
                        (self.game_area_left, self.game_area_top, 
                         self.game_area_width, self.game_area_height),10)
        
        # 分数
        score_text = self.game_font.render(f"接球次数: {self.catch_score}", True, (255, 255, 255))
        self.screen.blit(score_text, (self.game_area_left + 10, self.game_area_top + 10))
        
        # 游戏状态提示
        if self.catch_game_over:
            over_text = self.game_font.render("接球失败! 按R键重新开始", True, (255, 255, 255))
            self.screen.blit(over_text, (self.game_area_left + self.game_area_width//2 - 180, 
                                      self.game_area_top + self.game_area_height//2))
        elif self.catch_game_won:
            win_text = self.game_font.render(f"胜利! 连击数：12！按ESC退出游戏", True, (255, 255, 255))
            self.screen.blit(win_text, (self.game_area_left + self.game_area_width//2 - win_text.get_width()//2, 
                                      self.game_area_top + self.game_area_height//2 - 20))




    def dialog(self,screen):
        if self.textNum != self.last_played_textNum and self.gameMode == 1:
            if self.dialogNum == 1 and self.textNum in [1,3]:
                self.effectDialog.play()
            self.last_played_textNum = self.textNum

        if self.dialogNum==1:
            if self.textNum==1:
                music_manager.play_bgm("bgm_normal")
                PDialog.show_dialog_bug(self.dialogBug,"111",self.bug_shy,screen)  
            elif self.textNum==2:
                PDialog.show_dialog_player(self.dialogPlayer, "111", screen)
            elif self.textNum==3:
                PDialog.show_dialog_bug(self.dialogBug,"111",self.bug_happy,screen)

        if self.dialogNum==2:
            if self.textNum==1:
                music_manager.play_bgm("bgm_normal")
                PDialog.show_dialog_bug(self.dialogBug,"222",self.bug_shy,screen)  
            elif self.textNum==2:
                PDialog.show_dialog_player(self.dialogPlayer, "222", screen)
            elif self.textNum==3:
                PDialog.show_dialog_bug(self.dialogBug,"222",self.bug_happy,screen)

        if self.dialogNum==3:
            if self.textNum==1:
                music_manager.play_bgm("bgm_normal")
                PDialog.show_dialog_bug(self.dialogBug,"333",self.bug_shy,screen)  
            elif self.textNum==2:
                PDialog.show_dialog_player(self.dialogPlayer, "333", screen)
            elif self.textNum==3:
                PDialog.show_dialog_bug(self.dialogBug,"333",self.bug_happy,screen)                
                
        if self.dialogNum==4:
            if self.textNum==1:
                music_manager.play_bgm("bgm_normal")
                PDialog.show_dialog_bug(self.dialogBug,"444",self.bug_shy,screen)  
            elif self.textNum==2:
                PDialog.show_dialog_player(self.dialogPlayer, "444", screen)
            elif self.textNum==3:
                PDialog.show_dialog_bug(self.dialogBug,"444",self.bug_happy,screen)




    def handle_mouse_button_down(self, event):
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

                if self.is_clicked_start:
                    self.is_clicked_start_sleep = self.statebox.is_clicked_start_sleep((x,y), self.is_level_end)
                    if self.is_clicked_start_sleep:
                        music_manager.stop_bgm()
                        self.effectChangeLevel.play()

                if self.rightmenu.handle_left_click((x,y),self.right_menu_state):
                    self.right_menu_returnval=self.rightmenu.get_return_value()
                    if self.right_menu_returnval==0:
                        self.right_menu_state=1
                    elif self.right_menu_returnval==1 or self.right_menu_returnval==None:
                        self.right_menu_state=0
                    elif self.right_menu_returnval==5:
                        print("当前关卡禁用复制粘贴")

                if not self.tball_ismoving:
                    self.tball_ismoving=self.tball.is_clicked((x,y))

            if event.button==2:
                x,y=event.pos
                if self.tball_ismoving:
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
        self.is_password_get=self.password_window.check_password(7)
        
        # 接球游戏按键处理
        if self.gameMode == 2:
            if event.key == pygame.K_r and self.catch_game_over:
                self.reset_catch_game()
                self.paddle_width += 150
            elif event.key == pygame.K_p and not self.catch_game_won and not self.catch_game_over:
                self.catch_score = 12
                self.catch_game_won = True
            elif event.key == pygame.K_ESCAPE and self.catch_game_won:
                self.gameMode = 0
        
        if event.key == pygame.K_DOWN:
            if self.gameMode == 1:
                self.gameMode = 0
            elif self.gameMode == 0:
                self.gameMode = 1
            elif self.gameMode == 2:
                self.gameMode = 0
        if event.key==pygame.K_LEFT:
            self.gameMode=2
        if event.key==pygame.K_r:
            self.appicon.reset()




    def update(self):
        super().update()

        if self.gameMode == 2:
            self.update_catch_game()

        self.transition_over=self.transition.update()
        if self.isopen and not self.transition.is_active():
                self.transition.start(duration=500)

        if self.transition_over:
                self.isopen=False
                self.transition_over=False

        if self.gameMode==1:
            if self.textNum >= 4 and self.dialogNum == 1:
                print("dialog1 over")
                self.textNum = 0
                self.dialogNum = 2
                self.gameMode = 0
                self.right_menu_state=0
            if self.textNum >= 4 and self.dialogNum == 2:
                print("dialog2 over")
                self.textNum = 0
                self.dialogNum = 3
                self.gameMode = 0
                self.right_menu_state=5
            if self.textNum >= 4 and self.dialogNum == 3:
                print("dialog3 over")
                self.textNum = 0
                self.dialogNum = 4
                self.gameMode = 0
            if self.textNum >= 4 and self.dialogNum == 4:
                print("dialog4 over")
                self.textNum = 0
                self.dialogNum = 0
                self.gameMode = 0
                self.is_level_end=True

        elif self.gameMode==0:
            self.transition_end_over = self.transition_end.update()
            if self.is_level_end and self.is_clicked_start_sleep:
                if not self.transition_end.is_active():
                    self.transition_end.start(duration=2000,text="Day 5    --->    Day 6")

                if self.transition_end_over:
                    config.current_state = GameState.LEVEL7
                    self.transition_end_over = False




    def draw(self):
        self.screen.blit(self.bgside, (0, 0))
        self.screen.blit(self.bg, (200, 0))

        self.appicon.draw_icon(self.screen,15)
        self.appicon.draw_window(self.screen)

        self.statebox.draw_state_box(self.screen,True,False)
        date_text = self.font.render("Day 5", True, (255, 255, 255))
        self.screen.blit(date_text,(1380,910))

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

        if self.gameMode == 2:
            self.draw_catch_game()
        elif self.gameMode==1:
            self.dialog(self.screen)

        x, y = pygame.mouse.get_pos()
        self.screen.blit(self.mouse, (x - 4, y - 4))

        if self.isopen:
            self.transition.draw(0, 1, self.screen)

        if self.is_level_end and self.is_clicked_start_sleep:
            self.transition_end.draw(0, 0, self.screen)

        if config.current_state == GameState.LEVEL7:
            self.screen.fill((0, 0, 0))

        self.screen.blit(self.screen_black, (0, 0))