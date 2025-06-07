#应用图标管理、绘制
#可能也要关联对应窗口？
#关于文件夹嵌套考虑在列表加上前后项/父子项？

import pygame
from resource_manager import res_mgr

class AppIcon:
    def __init__(self):
        self.selected_icon = None
        self.display_window=None
        self.current_folder = None  # 当前打开的文件夹ID
        self.font=res_mgr.load_font("small", size=20)

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
            {"id": 1, "type": "folder", "image": "icon_1", "rect": (250, 50), 
             "text": "我的文件夹", "father": None, "sons": [6, 7]},
            
            {"id": 2, "type": "file", "image": "icon_2", "rect": (250, 200), 
             "text": "上锁文件夹", "father": None, "sons": []},
            
            {"id": 3, "type": "file", "image": "icon_3", "rect": (250, 350), 
             "text": "文档.txt", "father": None, "sons": []},

            {"id": 4, "type": "file", "image": "icon_4", "rect": (250, 500), 
             "text": "设置", "father": None, "sons": []},

            {"id": 5, "type": "file", "image": "icon_5", "rect": (250, 650), 
             "text": "回收站", "father": None, "sons": []},
            
            # 文件夹内图标 (father指向所属文件夹)
            {"id": 6, "type": "folder", "image": "icon_s_1", "rect": (680, 300), 
             "text": "子文件夹1", "father": 1, "sons": [ 9]},
            
            {"id": 7, "type": "folder", "image": "icon_s_1", "rect": (680, 360), 
             "text": "子文件夹2", "father": 1, "sons": [10]},
            
            {"id": 8, "type": "file", "image": "icon_s_1", "rect": (680, 420), 
             "text": "子文件夹3", "father": 1, "sons": []},
            
            {"id": 9, "type": "file", "image": "icon_s_3", "rect": (680, 480), 
             "text": "文档.txt", "father": 6, "sons": []},
            
            {"id": 10, "type": "file", "image": "icon_s_3", "rect": (680, 540), 
             "text": "图片.png", "father": 7, "sons": []}
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







    def draw_icon(self, screen):
        for icon in self.icon_data :
            if icon["id"]<6:
                screen.blit(icon["image"], icon["rect"])

    def draw_icon_s(self, screen):#我的文件夹中显示图标
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




    def is_clicked(self, pos):
        print(self.display_window)
        # 检查是否点击了返回按钮
        if self.display_window and self.back_button_rect.collidepoint(pos):
            self.go_back()
            return "back"
         # 检查是否点击了关闭按钮   
        if self.display_window and self.close_button_rect.collidepoint(pos):
            self.close_window()
            return "close"

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





    def draw_window(self, screen):
        #print("now:",self.display_window, "current folder:", self.current_folder)
        if self.display_window == 1:  # 文件夹窗口
            self.draw_window_1(screen)
            # 根据当前文件夹绘制内容
            if self.current_folder == 1:  # 我的文件夹
                self.draw_icon_s(screen)
            elif self.current_folder == 6:  # 子文件夹1
                self.draw_icon_son1(screen)
            elif self.current_folder == 7:  # 子文件夹2
                self.draw_icon_son2(screen)
        elif self.display_window == 3:
            self.draw_window_3(screen)
        elif self.display_window == 4:
            self.draw_window_4(screen)
