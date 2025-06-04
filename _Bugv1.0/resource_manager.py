#资源管理器，包括图片、音乐音效、字体
#全局单例res_mgr（图片 字体 音效）    music_manager（音乐） （用单例.方法（）调用）
# 图片 短音效在主函数load_xxx预载，在关卡get_xxx（“key”）使用
#长音乐load_sound载入  get_sound  play_bgm（“key”） stop_bgm() 在关卡中使用



import pygame
import os

class ResourceManager:
    def __init__(self):
        self._images = {}
        self._sounds={}
        self._fonts = {}


    #图片
    def load_image(self, key, path, scale=None):
        if key not in self._images:
            try:
                image = pygame.image.load(path).convert_alpha()
                if scale:
                    image = pygame.transform.scale(image, scale)
                self._images[key] = image
            except pygame.error:
                print(f"Error loading image: {path}")
                self._images[key] = pygame.Surface((50, 50), pygame.SRCALPHA)  # 粉色占位图
                self._images[key].fill((255, 0, 255))
        return self._images[key]

    def get_image(self, key):
        return self._images.get(key)


    #音效音乐
    def load_sound(self, key, path):
        if key not in self._sounds:
            try:
                sound = pygame.mixer.Sound(path)
                self._sounds[key] = sound
            except pygame.error:
                print(f"Error loading sound: {path}")
                self._sounds[key] = pygame.mixer.Sound('default.wav')
        return self._sounds[key]

    def get_sound(self, key):
        return self._sounds.get(key)
    

    #字体，记得是中文字体
    def load_font(self, key, path=None, size=36):#默认字体等线，找到合适的可以替
        path="_Bugv1.0/assets/font/Deng.ttf"
        if key not in self._fonts:
            self._fonts[key] = pygame.font.Font(path, size) if path else pygame.font.SysFont(None, size)
        return self._fonts[key]
    

res_mgr = ResourceManager()





#长音乐 类
class MusicManager:
    def __init__(self):
        self.current_bgm = None
    
    def play_bgm(self, bgm_name, loops=-1):
        """播放指定BGM"""
        if self.current_bgm != bgm_name:
            self.stop_bgm()
            bgm = res_mgr.get_sound(bgm_name)
            if bgm:
                bgm.play(loops=loops)
                self.current_bgm = bgm_name
    
    def stop_bgm(self):
        """停止当前BGM"""
        if self.current_bgm:
            res_mgr.get_sound(self.current_bgm).stop()
            self.current_bgm = None

music_manager = MusicManager()