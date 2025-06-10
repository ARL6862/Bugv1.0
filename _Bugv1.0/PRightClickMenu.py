#功能：右键鼠标，在鼠标处显示选项菜单

# menu_state-->外部传进来的参数，int类
# return_value-->传出去的参数（是否复制的bool 和 粘贴计数的int类型，用的都是这个）

#编辑者1：炸虾油
#6月8下午 宿舍开着门热死我了...
#是的老师，我们喜欢把注释当qq空间


import pygame
from resource_manager import res_mgr

class ContextMenu:
    def __init__(self, screen,menu_state):
        self.screen = screen
        self.visible = False
        self.pos = (0, 0)
        self.size=(160,40)
        self.rect = pygame.Rect(*self.pos, *self.size)
        self.menu_state = menu_state  # 默认状态，会被主函数覆盖
        self.return_value = None

        
        
        # 定义屏幕区域（去掉两边两条的那个区域），用来整菜单显示区域的逻辑
        self.CENTER_AREA_WIDTH = 1280
        self.CENTER_AREA_HEIGHT = 960
        self.CENTER_AREA_X = (screen.get_width() - self.CENTER_AREA_WIDTH) // 2
        self.CENTER_AREA_Y = (screen.get_height() - self.CENTER_AREA_HEIGHT) // 2
        self.CENTER_AREA_RECT = pygame.Rect(
            self.CENTER_AREA_X, self.CENTER_AREA_Y, 
            self.CENTER_AREA_WIDTH, self.CENTER_AREA_HEIGHT
        )
        
        # 菜单可能会显示的选项配置
        self.options = [
            {'text': "复制", 'rect': pygame.Rect(0, 0, 160, 40), 'action': 'copy'},
            {'text': "粘贴", 'rect': pygame.Rect(0, 0, 160, 40), 'action': 'paste'},
            {'text': "无可粘贴选项", 'rect': pygame.Rect(0, 0, 160, 40), 'action': 'no_paste'},
            {'text': "粘贴数达上限", 'rect': pygame.Rect(0, 0, 160, 40), 'action': 'paste_max'},
            {'text': "当前无操作权限", 'rect': pygame.Rect(0, 0, 160, 40), 'action': 'cant'}
        ]

        self.current_option=self.options[0]
        
        # 加载字体
        self.font = pygame.font.Font("_Bugv1.0/assets/font/Deng.ttf", 20)

    



    
    def show_menu(self, mouse_pos,menu_state):
        """右键显示菜单"""
        
        self.menu_state=menu_state
        self.visible = True
        #self.pos = mouse_pos

        print(self.current_option['rect'])

        
        if self.CENTER_AREA_RECT.collidepoint(mouse_pos):#点击屏幕范围内
            self.pos = mouse_pos
            self.return_value = None
                # 在区域内-->防止菜单溢出区域
            #menu_width = 160
            #menu_height = 40

            #max_x = self.CENTER_AREA_RECT.right - menu_width
            #max_y = self.CENTER_AREA_RECT.bottom - menu_height

           # new_x = min(max(mouse_pos[0], self.CENTER_AREA_RECT.left), max_x)
           # new_y = min(max(mouse_pos[1], self.CENTER_AREA_RECT.top), max_y)

            
        else:
            # 在区域外-->显示在游戏窗口外
            self.pos = (0, -50)

        self.rect=pygame.Rect(*self.pos,*self.size)
        self.options[self.menu_state]['rect'] = self.rect
        self.current_option['rect']=self.rect
        print(self.current_option['rect'])




    
    def handle_left_click(self, mouse_pos,menu_state):
        print(self.current_option['rect'])

        """处理左键点击不同情况"""
        if self.current_option['rect'].collidepoint(mouse_pos):
            self.menu_state=menu_state
            self.current_option = self.options[self.menu_state]
            
            if self.menu_state == 0:  #点击复制，返回True
                print("复制",self.menu_state )
                self.return_value = 0
            elif self.menu_state == 1:  #点击粘贴，返回1
                print("粘贴",self.menu_state )
                self.return_value = 1
            elif self.menu_state==4:
                print("禁用右键操作",self.menu_state )
                self.return_value=4

            self.visible = False
            return True
        return False
        


    
    def draw(self, mouse_pos):
        """绘制菜单"""
        #基于传进来的menu_state参数-->0:显示复制，1：显示粘贴，2：显示“无可粘贴选项”，3：显示“粘贴数达上限”
        if not self.visible:
            return
        
        # 绘制菜单背景
        pygame.draw.rect(self.screen, (240, 240, 240), self.rect)
        pygame.draw.rect(self.screen, (255, 192, 203), self.rect, 5)
        
        # 获取当前选项
        current_option = self.options[self.menu_state]
        
        # 设置文字颜色
        text_color = (0, 0, 0) if self.menu_state in [0, 1] else (255, 0, 0)
        
        # 可点击项的高亮效果
        
        #if self.menu_state in [0, 1] and current_option['rect'].collidepoint(mouse_pos):
            #pygame.draw.rect(self.screen, (255, 192, 203), current_option['rect'])
        
        # 渲染文字
        text_surface = self.font.render(current_option['text'], True, text_color)
        text_rect = text_surface.get_rect(center=current_option['rect'].center)
        self.screen.blit(text_surface, text_rect)
        
    
    def get_return_value(self):
        """获取返回值并重置"""
        val = self.return_value
        self.return_value = None
        return val
    
    def kkk(self):
        #print(self.current_option['rect'])
        return 





"""
在外部函数的调用方法：

# 在关卡函数中
menu = ContextMenu(screen)

# 设置状态
menu.menu_state = 0  # 或1/2/3

# 处理事件
menu.handle_event(event, mouse_pos)

# 绘制
menu.draw(mouse_pos)

# 获取返回值
val = menu.get_return_value()


"""




"""把引号删了就可以测了
PS:下面这些测试这个方法用的喵，和关卡连上了之后就可以删掉了
    def main():
    # 基本初始化
    pygame.init()
    pygame.mixer.init()
    pygame.mouse.set_visible(False)
    screen = pygame.display.set_mode((1680, 960))
    clock = pygame.time.Clock()
    
    # 创建菜单实例
    context_menu = ContextMenu(screen)
    
    running = True
    while running:
        mouse_pos = pygame.mouse.get_pos()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            # 传递事件给菜单处理
            context_menu.handle_event(event, mouse_pos)
        
        # 从主函数设置菜单状态（示例）
        context_menu.menu_state = 1  # 这里应该是从外部逻辑获取的值
        
        # 清屏
        screen.fill((0, 0, 0))
        
        # 绘制菜单
        context_menu.draw(mouse_pos)
        
        # 检查返回值
        return_val = context_menu.get_return_value()
        if return_val is not None:
            if isinstance(return_val, bool):  # 复制
                print(f"复制操作完成，返回值: {return_val}")
            elif isinstance(return_val, int):  # 粘贴
                print(f"粘贴操作完成，返回值: {return_val}")
        
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()
"""