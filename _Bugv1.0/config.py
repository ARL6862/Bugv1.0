# config.py
#配置文件，全局单例config，用来管理关卡切换
#切换方法：在main或关卡中设置config.current_state


from enum import Enum
from types import SimpleNamespace

class GameState(Enum):
    MENU = 0
    LEVEL1 = 1
    LEVEL2 = 2
    LEVEL3 = 3
    LEVEL4 = 4
    LEVEL5 = 5
    LEVEL6 = 6
    LEVEL7 = 7
    LEVEL8 = 8

config = SimpleNamespace()
config.current_state = GameState.MENU
