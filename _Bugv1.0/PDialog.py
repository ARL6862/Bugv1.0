import pygame


#感谢ds圣开源！！之打字机效果及自动换行文本显示
#使用show_dialog_player(dialog_img, dialog_text, screen)
#或show_dialog_bug(dialog_img, dialog_text, bug_img, screen)即可

# 对话框和文本位置常量
DIALOG_PLAYER_RECT = (350, 700)
DIALOG_PLAYER_TEXT_OFFSET = (50, 80)  # 相对于对话框的偏移量
DIALOG_BUG_RECT = (750, 100)
DIALOG_BUG_TEXT_OFFSET = (50, 60)     # 相对于对话框的偏移量
DIALOG_BUG_CHA_OFFSET = (600, -30)      # Bug立绘相对于对话框的偏移量
DIALOG_CONSOLE_RECT = (350, 200)
DIALOG_CONSOLE_TEXT_OFFSET = (50, 80)  # 相对于对话框的偏移量

class TypewriterText:
    def __init__(self, char_delay=30):
        self.full_text = ""          # 完整文本内容
        self.displayed_text = ""     # 当前显示的文本
        self.last_char_time = 0      # 上次添加字符的时间
        self.char_delay = char_delay # 字符显示间隔(毫秒)
        self.is_complete = False     # 是否显示完成
        self.wrapped_lines = []      # 换行后的文本行
    
    def set_text(self, text, font, max_width):
        """设置新文本并重置状态"""
        self.full_text = text
        self.displayed_text = ""
        self.last_char_time = pygame.time.get_ticks()
        self.is_complete = False
        self.wrapped_lines = self._wrap_text(text, font, max_width)
    
    def update(self):
        """更新显示的文字"""
        if not self.is_complete and len(self.displayed_text) < len(self.full_text):
            current_time = pygame.time.get_ticks()
            if current_time - self.last_char_time > self.char_delay:
                self.displayed_text = self.full_text[:len(self.displayed_text)+1]
                self.last_char_time = current_time
                if len(self.displayed_text) == len(self.full_text):
                    self.is_complete = True
    
    def draw(self, surface, font, pos, color, line_height=30):
        """在指定位置绘制当前文本"""
        # 计算当前应显示的行数
        displayed_length = len(self.displayed_text)
        current_length = 0
        lines_to_draw = []
        
        for line in self.wrapped_lines:
            if current_length >= displayed_length:
                break
            line_length = len(line)
            if current_length + line_length <= displayed_length:
                lines_to_draw.append(line)
            else:
                lines_to_draw.append(line[:displayed_length-current_length])
            current_length += line_length
        
        # 绘制文本行
        for i, line in enumerate(lines_to_draw):
            if color == 0:  # 默认字体白色
                text_surface = font.render(line, True, (255, 255, 255))
            else:  # Bug字体紫红色
                text_surface = font.render(line, True, (200, 0, 80))
            surface.blit(text_surface, (pos[0], pos[1] + i * line_height))
    
    def _wrap_text(self, text, font, max_width):
        """文本换行辅助函数"""
        words = text.replace('\n', ' \n ').split(' ')
        lines = []
        current_line = []
        
        for word in words:
            if word == '\n':  # 处理手动换行
                lines.append(' '.join(current_line))
                current_line = []
                continue
                
            test_line = ' '.join(current_line + [word])
            test_width = font.size(test_line)[0]
            
            if test_width <= max_width:
                current_line.append(word)
            else:
                if current_line:  # 当前行有内容则先保存
                    lines.append(' '.join(current_line))
                    current_line = []
                # 处理超长单词
                if font.size(word)[0] > max_width:
                    wrapped = self._split_long_word(word, font, max_width)
                    lines.extend(wrapped[:-1])
                    current_line = [wrapped[-1]]
                else:
                    current_line = [word]
        
        if current_line:  # 添加最后一行
            lines.append(' '.join(current_line))
        
        return lines
    
    def _split_long_word(self, word, font, max_width):
        """分割超长单词"""
        parts = []
        current_part = ""
        
        for char in word:
            test_part = current_part + char
            if font.size(test_part)[0] <= max_width:
                current_part = test_part
            else:
                parts.append(current_part)
                current_part = char
        
        if current_part:
            parts.append(current_part)
        
        return parts

# 创建全局的打字机效果实例
typewriter_player = TypewriterText()
typewriter_bug = TypewriterText()
typewriter_console = TypewriterText()

def show_dialog_player(dialog_img, dialog_text, screen):

    # 获取对话框尺寸
    dialog_width = dialog_img.get_width()
    font = pygame.font.Font("_Bugv1.0/assets/font/Deng.ttf", 28)
    
    # 如果传入新文本，重置打字机效果
    if typewriter_player.full_text != dialog_text:
        typewriter_player.set_text(dialog_text, font, dialog_width - 100)
    
    # 更新打字机效果
    typewriter_player.update()
    
    # 绘制对话框
    screen.blit(dialog_img, DIALOG_PLAYER_RECT)
    
    # 计算文本起始位置
    text_pos = (DIALOG_PLAYER_RECT[0] + DIALOG_PLAYER_TEXT_OFFSET[0],
                DIALOG_PLAYER_RECT[1] + DIALOG_PLAYER_TEXT_OFFSET[1])
    
    # 绘制文本
    typewriter_player.draw(screen, font, text_pos, 0)
    
    return typewriter_player.is_complete





def show_dialog_bug(dialog_img, dialog_text, bug_img, screen):

    # 获取对话框尺寸
    dialog_width = dialog_img.get_width()
    font = pygame.font.Font("_Bugv1.0/assets/font/Deng.ttf", 22)
    
    # 如果传入新文本，重置打字机效果
    if typewriter_bug.full_text != dialog_text:
        typewriter_bug.set_text(dialog_text, font, dialog_width - 100)
    
    # 更新打字机效果
    typewriter_bug.update()
    
    # 绘制对话框
    screen.blit(dialog_img, DIALOG_BUG_RECT)

    # 绘制Bug立绘
    bug_pos = (DIALOG_BUG_RECT[0] + DIALOG_BUG_CHA_OFFSET[0],
               DIALOG_BUG_RECT[1] + DIALOG_BUG_CHA_OFFSET[1])
    screen.blit(bug_img, bug_pos)

    # 计算文本起始位置
    text_pos = (DIALOG_BUG_RECT[0] + DIALOG_BUG_TEXT_OFFSET[0],
                DIALOG_BUG_RECT[1] + DIALOG_BUG_TEXT_OFFSET[1])
    
    # 绘制文本
    typewriter_bug.draw(screen, font, text_pos, 1)
    
    return typewriter_bug.is_complete




def show_dialog_console(dialog_img, dialog_text, screen):

    # 获取对话框尺寸
    dialog_width = dialog_img.get_width()
    font = pygame.font.Font("_Bugv1.0/assets/font/Deng.ttf", 22)
    
    # 如果传入新文本，重置打字机效果
    if typewriter_console.full_text != dialog_text:
        typewriter_console.set_text(dialog_text, font, dialog_width - 100)
    
    # 更新打字机效果
    typewriter_console.update()
    
    # 绘制对话框
    screen.blit(dialog_img, DIALOG_CONSOLE_RECT)

    # 计算文本起始位置
    text_pos = (DIALOG_CONSOLE_RECT[0] + DIALOG_CONSOLE_TEXT_OFFSET[0],
                DIALOG_CONSOLE_RECT[1] + DIALOG_CONSOLE_TEXT_OFFSET[1])
    
    # 绘制文本
    typewriter_console.draw(screen, font, text_pos, 0)
    
    return typewriter_console.is_complete







def show_dialog_bug_set(dialog_img, dialog_text, bug_img, screen,pos):

    DIALOG_BUG_RECT_SET = pos
    DIALOG_BUG_TEXT_SET_OFFSET = (50, 60)     # 相对于对话框的偏移量
    DIALOG_BUG_CHA_SET_OFFSET = (600, -30) 

    # 获取对话框尺寸
    dialog_width = dialog_img.get_width()
    font = pygame.font.Font("_Bugv1.0/assets/font/Deng.ttf", 22)
    
    # 如果传入新文本，重置打字机效果
    if typewriter_bug.full_text != dialog_text:
        typewriter_bug.set_text(dialog_text, font, dialog_width - 100)
    
    # 更新打字机效果
    typewriter_bug.update()
    
    # 绘制对话框
    screen.blit(dialog_img, DIALOG_BUG_RECT_SET)

    # 绘制Bug立绘
    bug_pos = (DIALOG_BUG_RECT_SET[0] + DIALOG_BUG_CHA_SET_OFFSET[0],
               DIALOG_BUG_RECT_SET[1] + DIALOG_BUG_CHA_SET_OFFSET[1])
    screen.blit(bug_img, bug_pos)

    # 计算文本起始位置
    text_pos = (DIALOG_BUG_RECT_SET[0] + DIALOG_BUG_TEXT_SET_OFFSET[0],
                DIALOG_BUG_RECT_SET[1] + DIALOG_BUG_TEXT_SET_OFFSET[1])
    
    # 绘制文本
    typewriter_bug.draw(screen, font, text_pos, 1)
    
    return typewriter_bug.is_complete

