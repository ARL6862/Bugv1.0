#关卡基类
#所有关卡代码中都需要继承这个类来进行事件处理、更新和绘制



import pygame

class BaseLevel:
    def __init__(self, screen, res_mgr):
        self.screen = screen
        self.res_mgr = res_mgr
        self._keys_pressed = pygame.key.get_pressed()
        self._events = []

    def handle_events(self, events):
        #处理事件列表
        for event in events:
            if event.type == pygame.MOUSEMOTION:
                self.handle_mouse_motion(event)#将单个事件传递给对应的处理函数
            elif event.type == pygame.KEYDOWN:
                self.handle_keydown(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.handle_mouse_button_down(event)


    #单个事件处理
    def handle_mouse_motion(self, event):
        #处理鼠标移动事件
        pass

    def handle_keydown(self, event):
        #处理按键按下事件
        pass

    def handle_mouse_button_down(self, event):
        #处理鼠标点击事件
        pass




    def update(self):
        #更新游戏状态
        self._keys_pressed = pygame.key.get_pressed()

    def draw(self):
        #绘制游戏，所有跟绘制相关的东西
        pass

    def run(self, events):
        #运行关卡逻辑，说白了就是把下面的函数串起来都跑一遍
        #events是当前帧的事件列表
        self._events = events
        self.handle_events(events)
        self.update()
        self.draw()



    #连续事件处理
    @property
    def keys_pressed(self):
        #获取当前按键状态
        return self._keys_pressed

    @property
    def events(self):
        #获取当前帧的事件列表
        return self._events