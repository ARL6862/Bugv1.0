#通用函数
#0.1版里搬过来的，目前暂时没用，别管了

import pygame
import sys
import os
import random
import ctypes
from datetime import datetime, timedelta

def GameInt():
    pygame.init()
    pygame.mouse.set_visible(False)#隐藏鼠标
    width, height = 1600, 960
    screen = pygame.display.set_mode((width, height))#NOFRAME隐藏窗口边框
    #pygame.display.set_caption("")

    return screen


class Bug(pygame.sprite.Sprite):
    #定义构造函数
    def __init__(self):
        # 调父类来初始化子类
        pygame.sprite.Sprite.__init__(self)
        # 加载图片
        self.image =pygame.image.load("images/characters/IMG_CHA_bug.png").convert_alpha()
        # 获取图片rect区域
        self.rect = self.image.get_rect()
        # 设置位置
        self.rect.topleft=(30,330)
        # 记录上次移动时间
        self.last_move_time = datetime.now()


def BugAction(bug,screen):
    current_time = datetime.now()
    # 如果距离上次移动时间超过5秒
    if current_time - bug.last_move_time >= timedelta(seconds=3):
        # 随机生成新位置
        screen_width, screen_height = screen.get_size()
        # 减去精灵的宽度和高度，确保不会超出屏幕
        new_x = random.randint(0, screen_width - bug.rect.width)
        new_y = random.randint(0, screen_height - bug.rect.height)
        bug.rect.topleft = (new_x, new_y)
        # 更新上次移动时间
        bug.last_move_time = current_time


        
def Images():#批量导入图片
    IMAGES = []
    for i in range(1, 3):
        filename = "images/icon/IMG_ICON_{}.png".format(i)
        image = pygame.image.load(filename)
        IMAGES[i-1]=image

        return IMAGES




def IconLoad(icon_data):
    for i in range(1, 4):  # 加载IMG_ICON_1.png到IMG_ICON_3.png
        try:
            filename = f"images/icon/IMG_ICON_{i}.png"
            image = pygame.image.load(filename).convert_alpha()
            rect = image.get_rect(topleft=(50, 50 + (i-1)*150))
            icon_data.append({"image": image, "rect": rect, "id": i})
        except pygame.error as e:
            print(f"无法加载图像 {filename}: {e}")
            # 创建占位图像
            placeholder = pygame.Surface((50, 50), pygame.SRCALPHA)
            placeholder.fill((255, 255, 255, 128))
            rect = image.get_rect(topleft=(50, 50 + (i-1)*150))
            icon_data.append({"image": placeholder, "rect": rect, "id": i})
    return icon_data


def WindowLoad(window_data):
    for i in range(1,3):
        try:
            filename = f"images/window/IMG_WD_{i}.jpg"
            image = pygame.image.load(filename).convert_alpha()
            rect = image.get_rect(topleft=(100, 100))
            window_data.append({"image": image, "rect": rect, "id": i})
        except pygame.error as e:
            print(f"无法加载图像 {filename}: {e}")
            # 创建占位图像
            placeholder = pygame.Surface((50, 50), pygame.SRCALPHA)
            placeholder.fill((255, 255, 255, 128))
            rect = image.get_rect(topleft=(100, 100))
            window_data.append({"image": placeholder, "rect": rect, "id": i})
        return window_data


def ItemLoad(item_data):
    for i in range(1, 2):  
        try:
            filename = f"images/item/IMG_ITEM_{i}.png"
            image = pygame.image.load(filename).convert_alpha()
            rect = image.get_rect(topleft=(400, 400 + (i-1)*150))
            item_data.append({"image": image, "rect": rect, "id": i,"isHold":False})
        except pygame.error as e:
            print(f"无法加载图像 {filename}: {e}")
            # 创建占位图像
            placeholder = pygame.Surface((400, 400), pygame.SRCALPHA)
            placeholder.fill((255, 255, 255, 128))
            rect = image.get_rect(topleft=(400, 400 + (i-1)*150))
            item_data.append({"image": placeholder, "rect": rect, "id": i})
    return item_data
