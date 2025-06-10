#应用图标管理、绘制   后来包括界面上常驻的一些东西也放这儿了 比如状态栏
#可能也要关联对应窗口？
#关于文件夹嵌套考虑在列表加上前后项/父子项？——然后程序员的一生就被毁了

import pygame
from resource_manager import res_mgr

class AppIcon:
    def __init__(self):
        self.selected_icon = None
        self.display_window=None
        self.current_folder = None  # 当前打开的文件夹ID
        self.font=res_mgr.load_font("small", size=20)
        self.font_username=res_mgr.load_font("username", size=40)

        self.icon_data = [] #桌面所有图标
        self.window_data = []#桌面图标对应窗口 1级

        self.icon_data_myfold = [] #桌面-我的文件夹内部图标
        self.window_data_myfold = []#桌面-我的文件夹内文件夹对应窗口 2级

        self.icon_data_mycon = []#桌面-我的电脑内图标

        # 定义按钮区域
        self.back_button_rect = pygame.Rect(600, 190, 85, 55)  # 返回按钮区域
        self.close_button_rect = pygame.Rect(1216, 178, 60, 60)  # 关闭按钮区域

        self.int_icon(res_mgr)
        self.int_window(res_mgr)

    def reset(self): #想着是防止bug卡死做的重置。。
        self.display_window = None
        self.selected_icon = None
        self.current_folder = None

        self.icon_data = [] #桌面所有图标
        self.window_data = []#桌面图标对应窗口 1级

        self.icon_data_s = [] #桌面-文件夹内部图标-try
        self.window_data_s = []#桌面-文件夹内文件夹对应窗口 try 2级

        self.icon_data_mycon = []#桌面-我的电脑内图标

        # 定义按钮区域
        self.back_button_rect = pygame.Rect(600, 190, 85, 55)  # 返回按钮区域
        self.close_button_rect = pygame.Rect(1216, 178, 60, 60)  # 关闭按钮区域

        self.int_icon(res_mgr)
        self.int_window(res_mgr)


    def int_icon(self,res_mgr):
        self.icon_data = [
            # 桌面图标 (father为None表示在桌面)
            {"id": 1, "type": "folder", "image": "icon_8", "rect": (250, 50), 
             "text": "我的电脑", "father": None, "sons": []},
            
            {"id": 2, "type": "folder", "image": "icon_4", "rect": (250, 200), 
             "text": "设置", "father": None, "sons": []},
            
            {"id": 3, "type": "folder", "image": "icon_1", "rect": (250, 350), 
             "text": "我的文件夹！", "father": None, "sons": [6,7,8]},

            {"id": 4, "type": "folder", "image": "icon_2", "rect": (250, 500), 
             "text": "也是我的文件夹！", "father": None, "sons": [9]},

            {"id": 5, "type": "folder", "image": "icon_3", "rect": (250, 650), 
             "text": "密码本.txt", "father": None, "sons": []},
            
            # 我的文件夹内图标 (father指向所属文件夹)
            {"id": 6, "type": "folder", "image": "icon_s_1", "rect": (680, 300), 
             "text": "好吃的！", "father": 3, "sons": []},
            
            {"id": 7, "type": "folder", "image": "icon_s_1", "rect": (680, 360), 
             "text": "xxx", "father": 3, "sons": []},
            
            {"id": 8, "type": "folder", "image": "icon_s_1", "rect": (680, 420), 
             "text": "xxx", "father": 3, "sons": []},
            
            {"id": 9, "type": "folder", "image": "icon_s_1", "rect": (680, 300), 
             "text": "新建文件夹", "father": 4, "sons": [10]},
            
            {"id": 10, "type": "folder", "image": "icon_s_1", "rect": (680, 300), 
             "text": "新建文件夹（1）", "father": 9, "sons": [11]},

             {"id": 11, "type": "folder", "image": "icon_s_1", "rect": (680, 300), 
             "text": "新建文件夹（2）", "father": 10, "sons": [12]},

             {"id": 12, "type": "folder", "image": "icon_s_5", "rect": (680, 300), 
             "text": "回收站", "father": 11, "sons": []}

             
        ]
        # 加载实际图片资源
        for icon in self.icon_data:
            size = (100, 100) if icon["father"] is None else (40, 40)
            icon["image"] = res_mgr.get_image(icon["image"]).copy()
            icon["image"] = pygame.transform.scale(icon["image"], size)
            icon["rect"] = pygame.Rect(*icon["rect"], *size)



    def int_window(self,res_mgr):
        self.load_window(res_mgr)


    def load_window(self, res_mgr):
        #可以加一些不同关卡的处理逻辑
        for i in range(1, 6):
            image = res_mgr.get_image(f"window_{i}")
            rect = image.get_rect(topleft=(550, 150))
            self.window_data.append({"image": image, "rect": rect, "id": i})





    def get_icons_in_current_folder(self):
        #获取当前文件夹下的所有图标
        if self.current_folder is None:  # 桌面
            return [icon for icon in self.icon_data if icon["father"] is None]
        else:
            return [icon for icon in self.icon_data if icon["father"] == self.current_folder]







    def draw_icon(self, screen,num):
        for icon in self.icon_data :
            if icon["id"]<=num:
                screen.blit(icon["image"], icon["rect"])
                icon_text = self.font.render(icon["text"], True, (255, 255, 255))
                text_rect = icon_text.get_rect()
                text_rect.centerx = icon["rect"].centerx
                text_rect.top = icon["rect"].bottom + 5
                screen.blit(icon_text, text_rect)


    def draw_icon_myfold(self, screen):#我的文件夹中显示图标
        for icon in self.icon_data:
            if icon["id"]>=6 and icon["id"]<=8:
                screen.blit(icon["image"], icon["rect"])
                icon_text = self.font.render(icon["text"], True, (0, 0, 0))
                screen.blit(icon_text, (icon["rect"].x+50,icon["rect"].y+10))

    def draw_icon_son1(self,screen):
        for icon in self.icon_data:
            if icon["id"]==9:
                screen.blit(icon["image"], icon["rect"])
                icon_text = self.font.render(icon["text"], True, (0, 0, 0))
                screen.blit(icon_text, (icon["rect"].x+50,icon["rect"].y+10))

    def draw_icon_son2(self,screen):
        for icon in self.icon_data:
            if icon["id"]==10:
                screen.blit(icon["image"], icon["rect"])
                icon_text = self.font.render(icon["text"], True, (0, 0, 0))
                screen.blit(icon_text, (icon["rect"].x+50,icon["rect"].y+10))

    def draw_icon_son3(self,screen):
        for icon in self.icon_data:
            if icon["id"]==11:
                screen.blit(icon["image"], icon["rect"])
                icon_text = self.font.render(icon["text"], True, (0, 0, 0))
                screen.blit(icon_text, (icon["rect"].x+50,icon["rect"].y+10))
                
    def draw_icon_son4(self,screen):
        for icon in self.icon_data:
            if icon["id"]==12:
                screen.blit(icon["image"], icon["rect"])
                icon_text = self.font.render(icon["text"], True, (0, 0, 0))
                screen.blit(icon_text, (icon["rect"].x+50,icon["rect"].y+10))




    def is_button_clicked(self, pos):
        #print(self.display_window)
        # 检查是否点击了返回按钮
        if self.display_window and self.back_button_rect.collidepoint(pos):
            self.go_back()
            return "back"
         # 检查是否点击了关闭按钮   
        if self.display_window and self.close_button_rect.collidepoint(pos):
            self.close_window()
            return "close"
        



    def is_clicked(self, pos):
        #print(self.display_window)
        # 检查图标点击
        for icon in self.get_icons_in_current_folder():
            if icon["rect"].collidepoint(pos):
                if icon["type"] == "folder":
                    self.open_folder(icon["id"])
                return icon["id"]
        return None
    





    def open_folder(self, folder_id):
        #打开文件夹
        print("打开文件夹",folder_id)
        self.current_folder = folder_id
        self.display_window = 1  # 固定使用窗口1显示文件夹内容



    """ 测试时发现：在桌面-点击我的文件夹-点击子文件夹1打开子文件夹1窗口，此时单击回退，
    会显示一个内部无图标的文件夹窗口，同时会先print“返回上一级文件夹 1”接着又print
    “返回上一级文件夹 None”，可能是连续使用了两次go_back（）方法；再单击一次回退，
    会直接回到桌面。 """
    #经过几个小时的痛苦折磨甚至ds老师也无法解决（梯子还死了用不了GPT）我郑重宣布不改了不改了哈哈哈哈哈。。。
    #反正嵌套的文件夹也没几个哈哈哈我在纠结什么
    #纠结怎么手搓出真正的操作系统吗那无敌了孩子们
    #老师你可不可以假装没看见有个回退按钮？？？

    #6.8补充：第二天醒来花了五分钟就解决了原因是is_clicked里既有检测应用图标的又有回退按钮的，可能干啥了导致返回值混乱了吧，拆开就好
    #目前是应用图标的click检测两次没影响，button click单独摘出来只进行一次，基本解决了  
    # 其实还有在最外层回退会变成空白文件夹的bug，懒得改了#已修复


    def go_back(self):
        #返回上一级文件夹
        if self.current_folder is None:
            print("返回上一级文件夹 桌面")
            self.close_window()
        else:
            current = next(icon for icon in self.icon_data if icon["id"] == self.current_folder)
            self.current_folder = current["father"]
            print(f"返回上一级文件夹 {self.current_folder}")
            # 保持窗口打开状态
            self.display_window = 1

    def close_window(self):
        #关闭窗口
        print("关闭窗口")
        self.display_window = None
        self.selected_icon = None
        self.current_folder = None










    def draw_window_1(self,screen):#文件夹
        screen.blit(self.window_data[0]["image"], self.window_data[0]["rect"])

    def draw_window_2(self,screen):#文本文档
        screen.blit(self.window_data[1]["image"], self.window_data[1]["rect"])

    def draw_window_3(self,screen):#占位-文本文档
        screen.blit(self.window_data[2]["image"], self.window_data[2]["rect"])

    def draw_window_4(self,screen):#设置
        screen.blit(self.window_data[3]["image"], self.window_data[3]["rect"])

    def draw_window_5(self,screen):#占位-文本文档
        screen.blit(self.window_data[4]["image"], self.window_data[4]["rect"])





    def draw_window(self, screen,password_num):
        #print("now:",self.display_window, "current folder:", self.current_folder)
        #if self.display_window == 1:  # 文件夹窗口
        
        # 根据当前文件夹绘制内容
        if self.current_folder == 1:  #我的电脑
            self.draw_window_1(screen)
            #self.draw_icon_s(screen)

        elif self.current_folder == 2:  #设置
            self.draw_window_4(screen)
            username_text = self.font_username.render("IAfOeraweB", True, (100, 0, 80))
            screen.blit(username_text,(780,220))
            #self.draw_icon_son1(screen)

        elif self.current_folder == 3:  #我的文件夹
            self.draw_window_1(screen)
            self.draw_icon_myfold(screen)

        elif self.current_folder == 4:  #上锁文件夹
            self.draw_window_1(screen)
            self.draw_icon_son1(screen)

        elif self.current_folder  == 5:#密码本 
            self.draw_window_2(screen)
            password_text_title = self.font_username.render("IAfOeraweB password :", True, (80, 0, 50))
            if password_num==0:
                password_text = self.font_username.render("[] [] [] [] [] [] [] [] [] []", True, (140, 0, 80))
            screen.blit(password_text_title,(730,200))
            screen.blit(password_text,(680,300))

        elif self.current_folder == 9:  #上锁文件夹-2
            self.draw_window_1(screen)
            self.draw_icon_son2(screen)
        
        elif self.current_folder == 10:  #上锁文件夹-3
            self.draw_window_1(screen)
            self.draw_icon_son3(screen)

        elif self.current_folder == 11:  #上锁文件夹-回收站
            self.draw_window_1(screen)
            self.draw_icon_son4(screen)
        

        #又是连点两次的bug。。#改掉了






class StateBox:
    def __init__(self):
        self.font=res_mgr.load_font("small", size=20)#1280 73
        self.state_box_on=res_mgr.get_image("control_online")
        self.state_box_on_end=res_mgr.get_image("control_online_end")
        self.state_box_off=res_mgr.get_image("control_offline")
        self.state_window_on=res_mgr.get_image("window_state_on")
        self.state_window_off=res_mgr.get_image("window_state_off")
        self.start_window_sleep=res_mgr.get_image("window_start_sleep")
        self.start_window_off=res_mgr.get_image("window_start_off")

        

        self.start_rect=pygame.Rect(200,880,200,80)
        self.state_rect=pygame.Rect(1180,880,300,80)
        self.state_window_rect=pygame.Rect(1080,480,400,400)
        self.state_window_wifi_rect=pygame.Rect(1137,565,100,100)
        self.start_window_rect=pygame.Rect(200,700,250,180) # 俩按钮加起来
        self.start_window_off_rect=pygame.Rect(200,700,250,80)
        self.start_window_sleep_rect=pygame.Rect(200,800,250,80)

        self.is_online=False
        self.is_click_state=False
        self.is_click_start=False

        self.font=res_mgr.load_font("small", size=20)
        self.font_wifiname=res_mgr.load_font("wifiname", size=30)




    def draw_state_box(self,screen,is_online,is_end):
        if is_online and not is_end:
            screen.blit(self.state_box_on, (200,887))
        elif is_end:
            screen.blit(self.state_box_on_end, (200,887))
        else:
            screen.blit(self.state_box_off, (200,887))


    


    def draw_state_window_L2(self,screen,is_online,wifitext):
        if is_online:
            screen.blit(self.state_window_on,(1080,480))
        else:
            screen.blit(self.state_window_off,(1080,480))
        text = self.font.render(wifitext, True, (100,0,80))
        screen.blit(text, (1280,620))


    def draw_state_window(self,screen):
        screen.blit(self.state_window_on,(1080,480))
        text = self.font.render("需要输入密码：", True, (100,0,80))
        screen.blit(text, (1260,620))
        text = self.font_wifiname.render("IAfOeraweB", True, (100,0,30))
        screen.blit(text, (1260,580))


    def draw_start_window(self,screen):
        screen.blit(self.start_window_off,(200,700))
        screen.blit(self.start_window_sleep,(200,800))





    def is_clicked_start(self,pos):
        if self.start_rect.collidepoint(pos):
            self.is_click_start=True
            return True
        elif self.is_click_start and not self.start_window_rect.collidepoint(pos):
            self.is_click_start=False
            return False
        elif self.is_click_start and self.start_window_rect.collidepoint(pos):
            return True
        return False
    
    def is_clicked_start_sleep(self,pos,is_level_end):
        if is_level_end and self.start_window_sleep_rect.collidepoint(pos) :
            return True
        return False





    def is_clicked_state(self,pos):
        if self.state_rect.collidepoint(pos):
            self.is_click_state=True
            #print("state")
            return True
        elif self.is_click_state and not self.state_window_rect.collidepoint(pos):
            self.is_click_state=False
            return False
        elif self.is_click_state and self.state_window_rect.collidepoint(pos):
            return True
        
    def is_clicked_state_wifi(self,pos,is_state_window_on):
        #print("wifi off")
        if is_state_window_on and self.state_window_wifi_rect.collidepoint(pos):
            print("wifi on")
            return True
        


    #还差个音量键
            




class TemperatureBall:
    def __init__(self):
        self.ball_60=res_mgr.get_image("Fball_60")
        self.ball_120=res_mgr.get_image("Fball_120")
        self.ball_pos=(1200,300)
        self.ball_size=(200,200)
        self.ball_rect = pygame.Rect(*self.ball_pos, *self.ball_size)

    def is_clicked(self,pos):

        return False
    
    def drop(self,pos):
        self.ball_pos=pos
        self.ball_rect = pygame.Rect(*self.ball_pos, *self.ball_size)


    def draw(self,screen,isTup=False):
        if isTup:
            screen.blit(self.ball_120,self.ball_pos)
        else:
            screen.blit(self.ball_60,self.ball_pos)
