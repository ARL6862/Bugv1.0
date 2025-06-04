#应用图标管理、绘制
#可能也要关联对应窗口？
#关于文件夹嵌套考虑在列表加上前后项/父子项？

import pygame
from resource_manager import res_mgr

class AppIcon:
    def __init__(self):
        self.selected_icon = None
        self.icon_data = []
        self.display_window=None
        self.window_data = []
        self.icon_data_s = []
        self.font=res_mgr.load_font("small", size=20)

    def load_icon(self, res_mgr):
        #可以加一些不同关卡的处理逻辑
        for i in range(1, 6):
            image = res_mgr.get_image(f"icon_{i}")
            rect = image.get_rect(topleft=(250, 50 + (i-1)*150))
            self.icon_data.append({"image": image, "rect": rect, "id": i})


    def draw_icon(self, screen):
        for icon in self.icon_data:

            screen.blit(icon["image"], icon["rect"])


    def is_clicked(self, pos):
        if any(icon["rect"].collidepoint(pos) for icon in self.icon_data):
            for icon in self.icon_data:
                if icon["rect"].collidepoint(pos):
                    
                    return icon["id"]
        return None
    


    def load_window(self, res_mgr):
        #可以加一些不同关卡的处理逻辑
        for i in range(1, 6):
            image = res_mgr.get_image(f"icon_s_{i}")
            rect = image.get_rect(topleft=(680, 300 + (i-1)*60))
            if i==1:
                text="新建文件夹"
            elif i==2:
                text="新建文件夹（1）"
            elif i==3:
                text="新建文件夹（2）"
            elif i==4:
                text="新建文件夹（3）"
            elif i==5:
                text="新建文件夹（4）"
            self.icon_data_s.append({"image": image, "rect": rect, "id": i,"text":text})
        for i in range(1, 6):
            image = res_mgr.get_image(f"window_{i}")
            rect = image.get_rect(topleft=(550, 150))
            self.window_data.append({"image": image, "rect": rect, "id": i})


    def draw_icon_s(self, screen):
        for icon in self.icon_data_s:
            screen.blit(icon["image"], icon["rect"])
            icon_text = self.font.render(icon["text"], True, (0, 0, 0))
            screen.blit(icon_text, (icon["rect"].x+50,icon["rect"].y+10))


    def draw_window_1(self,screen):
        screen.blit(self.window_data[0]["image"], self.window_data[0]["rect"])
        self.draw_icon_s(screen)

    def draw_window_2(self,screen):
        screen.blit(self.window_data[1]["image"], self.window_data[1]["rect"])

    def draw_window_3(self,screen):
        screen.blit(self.window_data[2]["image"], self.window_data[2]["rect"])

    def draw_window_4(self,screen):
        screen.blit(self.window_data[3]["image"], self.window_data[3]["rect"])

    def draw_window_5(self,screen):
        screen.blit(self.window_data[4]["image"], self.window_data[4]["rect"])


    def draw_window(self, screen):
        if self.display_window is not None:
            if self.display_window==1:
                # 在这里绘制窗口1
                self.draw_window_1(screen)
            elif self.display_window==3:
                # 在这里绘制窗口3
                self.draw_window_3(screen)
            elif self.display_window==4:
                # 在这里绘制窗口4
                self.draw_window_4(screen)
