#关卡几来着反正不是L3，接球游戏那关，还没优化只是搬过来测试



import pygame
import random
from .level_base import BaseLevel
from config import GameState, config

class Level6(BaseLevel):


    def __init__(self, screen, res_mgr):
        super().__init__(screen, res_mgr)
        #资源加载
        self.bg = res_mgr.get_image("bg_normal")
        self.bgside = res_mgr.get_image("bgside_normal")
        self.mouse = res_mgr.get_image("mouse_normal")

        self.screen_black = res_mgr.get_image("screen_black")

        self.font = res_mgr.load_font("default", size=36)
        self.large_font = res_mgr.load_font("large", size=72)
        
        # 游戏区域边界 (x=200到x=1480)
        self.game_area_left = 200
        self.game_area_right = 1480
        self.game_area_width = self.game_area_right - self.game_area_left
        
        # 游戏参数
        self.reset_game()
        self.paddle_speed = 10  # 平板移动速度
        self.ball_speed_increase = 0.5#每次反弹后增加的小球速度



    def reset_game(self):
        #方便失败重开时重置游戏状态

        # 平板参数
        self.paddle_width = 100
        self.paddle_height = 20
        self.paddle_x = self.game_area_left + (self.game_area_width - self.paddle_width) // 2
        self.paddle_y = self.screen.get_height() - 40
        
        # 小球参数
        self.ball_radius = 10
        self.ball_x = self.game_area_left + self.game_area_width // 2
        self.ball_y = self.screen.get_height() // 2
        self.ball_dx = 5 * random.choice([-1, 1])
        self.ball_dy = -5
        
        self.score = 0
        self.game_over = False
        self.game_won = False



    def handle_keydown(self, event):
        #处理键盘事件
        if event.key == pygame.K_r and self.game_over:
            self.reset_game()
            self.paddle_width += 150  # 失败后增加板长，防呆
        elif event.key == pygame.K_p and not self.game_won and not self.game_over:
            # 开发者快捷键直接胜利，免得演示时过不了丢人
            self.score = 12
            self.game_won = True
        elif event.key == pygame.K_ESCAPE and self.game_won:
            # 胜利后返回桌面，这块还没写
            print("返回桌面") 



    def update(self):
        super().update()
        
        if not self.game_over and not self.game_won:
            # 使用A/D键控制平板，限制在游戏区域内
            if self.keys_pressed[pygame.K_a] and self.paddle_x > self.game_area_left:
                self.paddle_x -= self.paddle_speed
            if self.keys_pressed[pygame.K_d] and self.paddle_x < self.game_area_right - self.paddle_width:
                self.paddle_x += self.paddle_speed
            
            self.update_ball()




    def update_ball(self):
        """更新小球逻辑"""
        self.ball_x += self.ball_dx
        self.ball_y += self.ball_dy
        
        # 墙壁碰撞 - 限制在游戏区域内
        if (self.ball_x <= self.game_area_left + self.ball_radius or 
            self.ball_x >= self.game_area_right - self.ball_radius):
            self.ball_dx *= -1
        if self.ball_y <= self.ball_radius:
            self.ball_dy *= -1
        
        # 平板碰撞
        if (self.ball_y + self.ball_radius >= self.paddle_y and 
            self.paddle_x <= self.ball_x <= self.paddle_x + self.paddle_width and 
            self.ball_dy > 0):
            
            self.ball_dy *= -1
            self.score += 1
            
            # 每反弹一次增加速度
            if self.ball_dx > 0:
                self.ball_dx += self.ball_speed_increase
            else:
                self.ball_dx -= self.ball_speed_increase
            self.ball_dy -= self.ball_speed_increase
            
            # 胜利条件：十二次连击
            if self.score >= 12:
                self.game_won = True
        
        # 掉落检测
        if self.ball_y >= self.screen.get_height() + self.ball_radius:
            self.game_over = True

    def draw(self):

        self.screen.blit(self.bgside, (0, 0))
        self.screen.blit(self.bg, (200, 0))
        
        
        # 绘制游戏区域边界(可视化边界，暂时没啥用，可以画个边框代替)
        pygame.draw.rect(self.screen, (0, 0, 0), 
                        (self.game_area_left, 0, 
                         self.game_area_width, self.screen.get_height()), 10)
        
        # 绘制平板和小球
        pygame.draw.rect(self.screen, (255, 255, 255), 
                         (self.paddle_x, self.paddle_y, self.paddle_width, self.paddle_height))
        pygame.draw.circle(self.screen, (255, 255, 255), 
                          (int(self.ball_x), int(self.ball_y)), self.ball_radius)
        
        # 分数
        score_text = self.font.render(f"接球次数: {self.score}", True, (255, 255, 255))
        self.screen.blit(score_text, (50, 150))
        
        # 游戏状态提示
        if self.game_over:
            over_text = self.font.render("接球失败! 按R键重新开始", True, (255, 255, 255))
            self.screen.blit(over_text, (self.screen.get_width()//2 - 180, self.screen.get_height()//2))
        elif self.game_won:# 胜利提示，也是密码提示，还得改
            win_text = self.font.render(f"胜利! 连击数：12！按ESC返回桌面", True, (255, 255, 255))
            self.screen.blit(win_text, (self.screen.get_width()//2 - win_text.get_width()//2, 
                                      self.screen.get_height()//2 - 20))

        # 鼠标
        x, y = pygame.mouse.get_pos()
        self.screen.blit(self.mouse, (x-4, y-4))

        self.screen.blit(self.screen_black, (0, 0))