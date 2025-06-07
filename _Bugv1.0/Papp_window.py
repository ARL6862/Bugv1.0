#应用图标管理、绘制
#可能也要关联对应窗口？
#关于文件夹嵌套考虑在列表加上前后项/父子项？

import pygame
from resource_manager import res_mgr

class AppIcon:
    def __init__(self):
        self.selected_icon = None
        self.display_window=None
        self.font=res_mgr.load_font("small", size=20)

        self.icon_data = [] #桌面所有图标
        self.window_data = []#桌面图标对应窗口 1级

        self.icon_data_s = [] #桌面-文件夹内部图标-try
        self.window_data_s = []#桌面-文件夹内文件夹对应窗口 try 2级

        self.icon_data_mycon = []#桌面-我的电脑内图标



        

    def load_icon(self, res_mgr):
        #可以加一些不同关卡的处理逻辑
        for i in [1, 2, 3, 4, 5]:
            image = res_mgr.get_image(f"icon_{i}")
            rect = image.get_rect(topleft=(250, 50 + (i-1)*150))
            self.icon_data.append({"image": image, "rect": rect, "id": i})

        for i in [6, 7, 8, 9, 10]:
            image = res_mgr.get_image(f"icon_s_1")
            rect = image.get_rect(topleft=(680, 300 + (i-1-5)*60))
            if i==6:
                text="新建文件夹"
            elif i==7:
                text="新建文件夹（1）"
            elif i==8:
                text="新建文件夹（2）"
            elif i==9:
                text="新建文件夹（3）"
            elif i==10:
                text="新建文件夹（4）"
            self.icon_data_s.append({"image": image, "rect": rect, "id": i,"text":text})


    def draw_icon(self, screen):
        for icon in self.icon_data:

            screen.blit(icon["image"], icon["rect"])

    
    def draw_icon_s(self, screen):
        for icon in self.icon_data_s:
            screen.blit(icon["image"], icon["rect"])
            icon_text = self.font.render(icon["text"], True, (0, 0, 0))
            screen.blit(icon_text, (icon["rect"].x+50,icon["rect"].y+10))


    def is_clicked(self, pos):

        if any(icon["rect"].collidepoint(pos) for icon in self.icon_data):
            for icon in self.icon_data:
                if icon["rect"].collidepoint(pos):
                    print(icon["id"])
                    return icon["id"]
                    

        #print("666")
        if any(icon["rect"].collidepoint(pos) for icon in self.icon_data_s):
            for icon in self.icon_data_s:
                if icon["rect"].collidepoint(pos):    
                    print(icon["id"])
                    return icon["id"]
            
        return None
    




    def load_window(self, res_mgr):
        #可以加一些不同关卡的处理逻辑
        for i in range(1, 6):
            image = res_mgr.get_image(f"window_{i}")
            rect = image.get_rect(topleft=(550, 150))
            self.window_data.append({"image": image, "rect": rect, "id": i})






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
        if self.display_window is not None:
            if self.display_window==1:
                # 在这里绘制窗口1
                self.draw_window_1(screen)
                self.draw_icon_s(screen)
            elif self.display_window==3:
                # 在这里绘制窗口3
                self.draw_window_3(screen)
            elif self.display_window==4:
                # 在这里绘制窗口4
                self.draw_window_4(screen)



            if self.display_window==6:
                # 在这里绘制窗口6/新建文件夹
                self.draw_window_1(screen)

                print("新建文件夹")
            elif self.display_window==7:
                # 在这里绘制窗口7/新建文件夹1
                self.draw_window_1(screen)

                print("新建文件夹1")
            elif self.display_window==8:
                # 在这里绘制窗口8/新建文件夹2
                self.draw_window_1(screen)

                print("新建文件夹2")

    

