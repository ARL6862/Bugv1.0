#主函数，游戏唯一入口，测试运行此文件
#主循环+资源预载


#基本已完成


import pygame
import random
from config import GameState, config
from resource_manager import res_mgr,music_manager
from levels.L1 import Level1
from levels.L2 import Level2
from levels.L3 import Level3 
from levels.L4 import Level4
from levels.L5 import Level5 
from levels.L6 import Level6 
from levels.L7 import Level7
from levels.L8 import Level8 



def preload_resources():
    #预加载所有资源
    res_mgr.load_image("bg_L1", "_Bugv1.0/assets/background/IMG_BG_1.png", (1280, 960))#关卡1开机背景
    res_mgr.load_image("bg_L1_2", "_Bugv1.0/assets/background/IMG_BG_1_2.png", (1280, 960))#关卡1开机背景-欢迎
    res_mgr.load_image("bg_normal", "_Bugv1.0/assets/background/IMG_BG_2.png", (1280, 960))#正常背景

    res_mgr.load_image("bgside_normal", "_Bugv1.0/assets/background/IMG_BGSIDE_1.jpg", (1680, 960))#正常底图

    res_mgr.load_image("icon_1", "_Bugv1.0/assets/icon/IMG_ICON_1.png", (100, 100))#文件夹
    res_mgr.load_image("icon_2", "_Bugv1.0/assets/icon/IMG_ICON_2.png", (100, 100))#上锁文件夹
    res_mgr.load_image("icon_3", "_Bugv1.0/assets/icon/IMG_ICON_3.png", (100, 100))#文本文档
    res_mgr.load_image("icon_4", "_Bugv1.0/assets/icon/IMG_ICON_4.png", (100, 100))#设置
    res_mgr.load_image("icon_5", "_Bugv1.0/assets/icon/IMG_ICON_5.png", (100, 100))#回收站

    res_mgr.load_image("icon_s_1", "_Bugv1.0/assets/icon/IMG_ICON_1.png", (40, 40))#文件夹 小
    res_mgr.load_image("icon_s_2", "_Bugv1.0/assets/icon/IMG_ICON_2.png", (40, 40))#上锁文件夹
    res_mgr.load_image("icon_s_3", "_Bugv1.0/assets/icon/IMG_ICON_3.png", (40, 40))#文本文档
    res_mgr.load_image("icon_s_4", "_Bugv1.0/assets/icon/IMG_ICON_4.png", (40, 40))#设置
    res_mgr.load_image("icon_s_5", "_Bugv1.0/assets/icon/IMG_ICON_5.png", (40, 40))#回收站

    res_mgr.load_image("window_1", "_Bugv1.0/assets/window/IMG_WIN_1.png", (772, 640))#窗口 文件夹
    res_mgr.load_image("window_2", "_Bugv1.0/assets/window/IMG_WIN_2.png", (772, 640))#窗口 上锁文件夹 占位
    res_mgr.load_image("window_3", "_Bugv1.0/assets/window/IMG_WIN_3.png", (772, 640))#窗口 文本文档
    res_mgr.load_image("window_4", "_Bugv1.0/assets/window/IMG_WIN_4.png", (772, 640))#窗口 设置
    res_mgr.load_image("window_5", "_Bugv1.0/assets/window/IMG_WIN_5.png", (772, 640))#窗口 回收站 占位
    res_mgr.load_image("window_state_on", "_Bugv1.0/assets/window/IMG_WIN_STATE_ON.png", (400, 400))#状态栏右侧 窗口 联网
    res_mgr.load_image("window_state_off", "_Bugv1.0/assets/window/IMG_WIN_STATE_OFF.png", (400, 400))#状态栏右侧 窗口 断网


    #bug七个表情差分
    res_mgr.load_image("bug_normal", "_Bugv1.0/assets/character/IMG_BUG_NORMAL.png", (100, 114))#bug立绘 正常
    res_mgr.load_image("bug_happy", "_Bugv1.0/assets/character/IMG_BUG_HAPPY.png", (100, 114))#bug立绘 高兴
    res_mgr.load_image("bug_angry", "_Bugv1.0/assets/character/IMG_BUG_ANGRY.png", (100, 114))#bug立绘 生气
    res_mgr.load_image("bug_sad", "_Bugv1.0/assets/character/IMG_BUG_SAD.png", (100, 114))#bug立绘 伤心
    res_mgr.load_image("bug_shy", "_Bugv1.0/assets/character/IMG_BUG_SHY.png", (100, 114))#bug立绘 害羞
    res_mgr.load_image("bug_silence", "_Bugv1.0/assets/character/IMG_BUG_SILENCE.png", (100, 114))#bug立绘 沉默
    res_mgr.load_image("bug_scared", "_Bugv1.0/assets/character/IMG_BUG_SCARED.png", (100, 114))#bug立绘 害怕

    res_mgr.load_image("mouse_normal", "_Bugv1.0/assets/character/IMG_MOUSE_1.png", (30, 43))#鼠标 正常
    res_mgr.load_image("mouse_zoom", "_Bugv1.0/assets/character/IMG_MOUSE_2.png", (30, 43))#鼠标 放大镜

    res_mgr.load_image("dialog_bug", "_Bugv1.0/assets/else/IMG_DIA_BUG.png", (660, 260))#bug对话框
    res_mgr.load_image("dialog_player", "_Bugv1.0/assets/else/IMG_DIA_PLAYER.png", (973, 240))#player对话框

    res_mgr.load_image("control_online", "_Bugv1.0/assets/else/IMG_CONTROL_ONLINE.png", (1280, 73))#控制栏 联网
    res_mgr.load_image("control_offline", "_Bugv1.0/assets/else/IMG_CONTROL_OFFLINE.png", (1280, 73))#控制栏 离线

    res_mgr.load_image("item_example", "_Bugv1.0/assets/item/IMG_ITEM_1.png", (50,50))#道具 示例
    res_mgr.load_image("item_wakeup", "_Bugv1.0/assets/item/IMG_ITEM_WAKEUP.png", (50,50))#道具 额其实是小图标 开机

    res_mgr.load_image("screen_black", "_Bugv1.0/assets/else/IMG_SCREEN_BLACK.png", (1680, 960))#暗角,还需要优化

    res_mgr.load_image("button_ok", "_Bugv1.0/assets/else/IMG_BUTTON_OK.png", (130, 80))#确认按钮，L1
    res_mgr.load_image("inputbox", "_Bugv1.0/assets/else/IMG_INPUTBOX.png", (500, 80))#输入框，L1










    #音乐音效
    res_mgr.load_sound("bgm_normal", "_Bugv1.0/assets/sound/bgm_Far.mp3")#正常道中bgm
    res_mgr.load_sound("bgm_error", "_Bugv1.0/assets/sound/bgm_Kittycity.mp3")#真结局道中bgm

    res_mgr.load_sound("effect_dialog", "_Bugv1.0/assets/sound/effect_po.mp3")#对话音效
    res_mgr.load_sound("effect_wakeup", "_Bugv1.0/assets/sound/effect_wakeup.mp3")#开机音效



def main():

    #基本初始化
    pygame.init()
    pygame.mixer.init()
    pygame.mouse.set_visible(False)#隐藏鼠标
    screen = pygame.display.set_mode((1680, 960))
    clock = pygame.time.Clock()
    preload_resources()
    pygame.display.set_icon(res_mgr.get_image("bug_normal"))  # 设置窗口图标
    pygame.display.set_caption("Bug Game")  # 设置窗口标题
    img_wakeup=res_mgr.get_image("item_wakeup")

    

    #关卡列表
    levels = {
        GameState.LEVEL1: Level1(screen, res_mgr),
        GameState.LEVEL2: Level2(screen, res_mgr),
        GameState.LEVEL3: Level3(screen, res_mgr),
        GameState.LEVEL4: Level4(screen, res_mgr),
        GameState.LEVEL5: Level5(screen, res_mgr),
        GameState.LEVEL6: Level6(screen, res_mgr),
        GameState.LEVEL7: Level7(screen, res_mgr),
        GameState.LEVEL8: Level8(screen, res_mgr)
    }



    running=True
    prev_state = None
    while running:
        frame_events = []  # 收集当前帧的所有事件
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            frame_events.append(event)  # 收集事件


            #！！！这里方便测试，用方向键右键进行快捷关卡切换，最后会删
            #切换关卡时放音乐的话注意只有按右键行 得改
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:  # 切换关卡
                    if config.current_state == GameState.LEVEL1:
                        music_manager.stop_bgm()#顺便清除上一关bgmn并播放下一关bgm，其实bgm切换只在结局分支有，之后再改吧
                        config.current_state = GameState.LEVEL2
                        music_manager.play_bgm("bgm_normal")
                    elif config.current_state == GameState.LEVEL2:
                        music_manager.stop_bgm()
                        config.current_state = GameState.LEVEL3
                        music_manager.play_bgm("bgm_error")
                    elif config.current_state == GameState.LEVEL3:
                        music_manager.stop_bgm()
                        config.current_state = GameState.LEVEL4
                    elif config.current_state == GameState.LEVEL4:
                        music_manager.stop_bgm()
                        config.current_state = GameState.LEVEL5
                    elif config.current_state == GameState.LEVEL5:
                        music_manager.stop_bgm()
                        config.current_state = GameState.LEVEL6
                    elif config.current_state == GameState.LEVEL6:
                        music_manager.stop_bgm()
                        config.current_state = GameState.LEVEL7
                    elif config.current_state == GameState.LEVEL7:
                        music_manager.stop_bgm()
                        config.current_state = GameState.LEVEL8
                    elif config.current_state == GameState.LEVEL8:
                        music_manager.stop_bgm()
                        config.current_state = GameState.LEVEL1

                        
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if img_wakeup.get_rect(center=(screen.get_width()//2, screen.get_height()//2)).collidepoint(event.pos):
                    if config.current_state == GameState.MENU:
                        music_manager.stop_bgm()
                        config.current_state = GameState.LEVEL1


        if config.current_state in levels:
            levels[config.current_state].run(frame_events)  # 如果当前关卡为x则把事件处理的权利给x（即传递事件列表）
        else:  
            screen.fill((0, 0, 0))
            screen.blit(img_wakeup, img_wakeup.get_rect(center=(screen.get_width()//2, screen.get_height()//2)))

                # 绘制鼠标指针
        x, y = pygame.mouse.get_pos()
        screen.blit(res_mgr.get_image("mouse_normal"), (x-4, y-4))

        pygame.display.flip()
        clock.tick(60)


main()