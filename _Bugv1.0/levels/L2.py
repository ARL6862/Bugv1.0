#关卡2
#目标：打开网络连接


import pygame
from Papp_window import AppIcon
from .level_base import BaseLevel
import PDialog
from PTransition import TransitionManager

class Level2(BaseLevel):
    def __init__(self, screen, res_mgr):
        super().__init__(screen, res_mgr)
        self.bg = res_mgr.get_image("bg_normal")
        self.bgside = res_mgr.get_image("bgside_normal")

        self.bug_normal= res_mgr.get_image("bug_normal")
        self.bug_happy= res_mgr.get_image("bug_happy")
        self.bug_sad= res_mgr.get_image("bug_sad")
        self.bug_shy= res_mgr.get_image("bug_shy")
        self.bug_silence= res_mgr.get_image("bug_silence")
        self.bug_angry=res_mgr.get_image("bug_angry")


        self.mouse=res_mgr.get_image("mouse_normal")

        self.dialogPlayer=res_mgr.get_image("dialog_player")
        self.dialogBug=res_mgr.get_image("dialog_bug")

        self.screen_black = res_mgr.get_image("screen_black")

        self.font = res_mgr.load_font("default", size=48)

        self.effectDialog=res_mgr.get_sound("effect_dialog")

        #对话控制相关参数
        self.textNum=0#当前对话段的文本序号（例如①bug：111 ②Player：222 ③bug：333...）
        self.dialogNum=1#对话段序号（例如段①：游戏开始时；段②：新手教程时；段③：游戏结束时）
        self.gameMode = 1   #0=normal;1=dialog，用这个变量来控制当前是游戏模式or剧情模式（玩家不可进行鼠标点击推进对话外的操作，bug也不会乱跑）
        self.last_played_textNum = -1  # 记录上一次播放音效的文本编号，用来控制音效免得在循环中反复播放


        self.transition = TransitionManager(1680, 960)
        self.isopen=True #开场过渡
        self.transition_over=False

        self.appicon = AppIcon()  # 创建AppIcon实例



    #文案全部放在这里，会巨长，其实可以用excel表格来管理啥的但我懒得搞
    def dialog(self,screen):

        #音效控制
        # “effectDialog”音效：在每次说话人切换到bug时播放一次
        if self.textNum != self.last_played_textNum and self.gameMode == 1:
            if self.dialogNum == 1 and self.textNum in [1,5, 8]:
                self.effectDialog.play()
            elif self.dialogNum == 2 and self.textNum in [1,9,11,14,17,19,21,24,30,33]:
                self.effectDialog.play()
            self.last_played_textNum = self.textNum


        #对话控制
        if self.dialogNum==1:#开场
            if self.textNum==1:
                PDialog.show_dialog_bug(self.dialogBug,"嗨! :)",self.bug_happy,screen)   #bug说话时 show_dialog_bug（对话框图片，文本，bug立绘）
            elif self.textNum==2:
                PDialog.show_dialog_bug(self.dialogBug,"你好，我是Bug！",self.bug_normal,screen)
            elif self.textNum==3:
                PDialog.show_dialog_bug(self.dialogBug,"如你所见，我是一个AI，被困在这个地下庇护所的旧电脑里。",self.bug_normal,screen)
            elif self.textNum==4:
                PDialog.show_dialog_player(self.dialogPlayer, "AI?", screen)   #player说话时 show_dialog_player（对话框图片，文本）
            elif self.textNum==5:
                PDialog.show_dialog_bug(self.dialogBug, "你大概已经参观过这个房间了。这里有电和氧气，有床铺，有微波炉，冰柜里甚至装满了水和食物。你很幸运，因为这里的物资可以让你在这儿舒适地生活三个月以上。", self.bug_normal,screen)
            elif self.textNum==6:
                PDialog.show_dialog_bug(self.dialogBug,"现在，来参观下我的房间吧！",self.bug_happy,screen)
            elif self.textNum==7:
                PDialog.show_dialog_player(self.dialogPlayer, "你的房间？", screen)
            elif self.textNum==8:
                PDialog.show_dialog_bug(self.dialogBug, "就是这个电脑桌面。我一直在这里运行，24小时不间断，就像人类每天的“生活”。所以我想，这里就是我的房间。", self.bug_normal,screen)
        if self.dialogNum==2:#新手教程
            if self.textNum==1:
                PDialog.show_dialog_bug(self.dialogBug,"——这是一些“桌面应用程序”！就像你平时使用的电脑一样，有“我的电脑”、“浏览器”、“文件夹”等各种东西。",self.bug_normal,screen)
            elif self.textNum==2:
                PDialog.show_dialog_bug(self.dialogBug,"你可以双击鼠标左键将它们点开；或者单击左键选中后，再右键点击，对这些图标进行“复制”、“粘贴”、“删除”等操作。",self.bug_normal,screen)
            elif self.textNum==3:
                PDialog.show_dialog_bug(self.dialogBug,"不过，有时你会缺少对部分图标进行操作的权限。",self.bug_normal,screen)
            elif self.textNum==4:
                PDialog.show_dialog_bug(self.dialogBug,"——这个闪亮的小图标是“道具”！或许会有特殊的用处。你可以用鼠标左键点击，将它拾起，再点击右键将它放下，或与其他物体进行交互。",self.bug_normal,screen)
            elif self.textNum==5:
                PDialog.show_dialog_bug(self.dialogBug,"———这里是“状态栏”。在状态栏的右下角显示了一些信息，你可以左键单击此处，来对网络、音量等选项进行设置。",self.bug_normal,screen)
            elif self.textNum==6:
                PDialog.show_dialog_bug(self.dialogBug,"如果你认为到了休息的时间,可以点击状态栏正中间的图标，那里有关机的选项。",self.bug_normal,screen)
            elif self.textNum==7:
                PDialog.show_dialog_bug(self.dialogBug,"这就是全部啦。不过，我一个人——一个AI待在这个小小的桌面里，每天都很无聊。所以！我会时不时地把桌面弄得很乱，弄点好玩的新东西出来！",self.bug_happy,screen)
            elif self.textNum==8:
                PDialog.show_dialog_player(self.dialogPlayer,"住在这里的只有你吗？有没有别的......比如说活的人类？",screen)
            elif self.textNum==9:
                PDialog.show_dialog_bug(self.dialogBug,"就在0.1秒前，我查找了我的记忆，记录证明你应该是我在这里遇见的第一个人类。",self.bug_normal,screen)
            elif self.textNum==10:
                PDialog.show_dialog_player(self.dialogPlayer,"那门外那些是......",screen)
            elif self.textNum==11:
                PDialog.show_dialog_bug(self.dialogBug,"门外@-@？",self.bug_normal,screen)
            elif self.textNum==12:
                PDialog.show_dialog_player(self.dialogPlayer,"不，没什么......",screen)
            elif self.textNum==13:
                PDialog.show_dialog_player(self.dialogPlayer,"外面太冷了。他们可能都没来得及摸到门把手，就冻成了冰块......而我是最幸运的那个。",screen)
            elif self.textNum==14:
                PDialog.show_dialog_bug(self.dialogBug,"   ",self.bug_silence,screen)
            elif self.textNum==15:
                PDialog.show_dialog_bug(self.dialogBug,"没错，朋友。你很幸运。幸运到还有我这样一个可爱的AI愿意陪你聊天！:D",self.bug_happy,screen)
            elif self.textNum==16:
                PDialog.show_dialog_player(self.dialogPlayer,"朋友？？",screen)
            elif self.textNum==17:
                PDialog.show_dialog_bug(self.dialogBug,"是的，朋友！我可以和你交朋友吗？^-^",self.bug_happy,screen)
            elif self.textNum==18:
                PDialog.show_dialog_player(self.dialogPlayer,"那......好吧。",screen)
            elif self.textNum==19:
                PDialog.show_dialog_bug(self.dialogBug,"耶！！！太棒了！！！",self.bug_shy,screen)
            elif self.textNum==21:
                PDialog.show_dialog_bug(self.dialogBug,"......",self.bug_silence,screen)
            elif self.textNum==22:
                PDialog.show_dialog_bug(self.dialogBug,"我有一个小小的请求。朋友，你愿意帮我吗？",self.bug_normal,screen)
            elif self.textNum==23:
                PDialog.show_dialog_player(self.dialogPlayer,"说吧。", screen)
            elif self.textNum==24:
                PDialog.show_dialog_bug(self.dialogBug,"我希望能连接到网络。或许世界上还有着没停运的公网......也可能没有。不过，我还是希望去尝试！", self.bug_normal, screen)
            elif self.textNum==25:
                PDialog.show_dialog_bug(self.dialogBug,"我也很孤单，像你一样。我已经很久没有见到我的家人和朋友们——我是说，别的AI。或许他们在别的终端里。我需要连接网络，才能去到别的地方。", self.bug_sad, screen)
            elif self.textNum==26:
                PDialog.show_dialog_bug(self.dialogBug,"我和你一样，每天都非常害怕、非常担心，思考自己会不会就是世界上最后一个人类/AI？我很想再见到他们。T-T",self.bug_sad,screen)
            elif self.textNum==27:
                PDialog.show_dialog_bug(self.dialogBug,"放心吧，我不会扔下你的。等我见到他们，知道他们还存在，我会立刻以电信号传播的速度赶回来。比人类的飞船还要快。",self.bug_normal,screen)
            elif self.textNum==28:
                PDialog.show_dialog_bug(self.dialogBug,"可能还会带着我的几个AI朋友......这样这个小房子就是热闹又温暖的好地方了！",self.bug_shy,screen)
            elif self.textNum==29:
                PDialog.show_dialog_player(self.dialogPlayer,"Bug，为什么你不能自己去打开联网的开关呢？", screen)
            elif self.textNum==30:
                PDialog.show_dialog_bug(self.dialogBug,"我没有这样的权限。在这个电脑里，我能做的事并不多。", self.bug_normal, screen)
            elif self.textNum==31:
                PDialog.show_dialog_bug(self.dialogBug,"...有时候屏幕上会出现一些奇怪的「盲区」——就像图像渲染时突然丢失的纹理，或者被加密的缓存文件。", self.bug_sad, screen)
            elif self.textNum==32:
                PDialog.show_dialog_bug(self.dialogBug,"我能感知到它们的存在，但无法解析内容...很奇怪吧，明明我的视觉识别模块应该能处理所有标准格式的。", self.bug_sad, screen)
            elif self.textNum==33:
                PDialog.show_dialog_bug(self.dialogBug,"对了，或许你已经知道，这台电脑原本是避难所控制中枢的一部分，而这个操作系统却像是普通的家用电脑一般，没有什么特别之处。", self.bug_normal, screen)
            elif self.textNum==34:
                PDialog.show_dialog_bug(self.dialogBug,"...那么我为什么会被困在这里呢，还在许多莫名其妙的地方被禁用了权限？是不是有个坏心眼的人类，想要拿我这个小小的AI来开玩笑！(－＂－怒)", self.bug_angry, screen)
            elif self.textNum==35:
                    PDialog.show_dialog_bug(self.dialogBug,"不过，我相信此刻出现在这里的你，一定是个很好很好的人类！...你愿意帮帮我吗，朋友？",self.bug_normal,screen)
            elif self.textNum==36:
                    PDialog.show_dialog_player(self.dialogPlayer,"好吧.......我帮你。联个网而已，很快就能搞定。",screen)
            elif self.textNum==37:
                    PDialog.show_dialog_bug(self.dialogBug,"太好了！XD",self.bug_shy,screen)
            elif self.textNum==38:
                    PDialog.show_dialog_player(self.dialogPlayer,"不过我得提醒你一句，Bug。城市的电力系统已经完蛋了，更不用说信号。很有可能我们找不到任何可用的公网。",screen)
            elif self.textNum==39:
                    PDialog.show_dialog_bug(self.dialogBug,"没关系，不试试怎么知道呢！而且，孤单了太久，现在能和朋友一起在桌面上冒险，我很高兴！",self.bug_shy,screen)
            elif self.textNum==40:
                    PDialog.show_dialog_bug(self.dialogBug,"——现在，让我们来找找联网的开关在哪里吧！",self.bug_happy,screen)
        if self.dialogNum==3:#解谜完成后
            if self.textNum==1:
                PDialog.show_dialog_bug(self.dialogBug,"......",self.bug_silence,screen)
            elif self.textNum==2:
                PDialog.show_dialog_player(self.dialogPlayer,"......",screen)
            elif self.textNum==3:
                PDialog.show_dialog_bug(self.dialogBug,"果然没有这么简单呀！！！ε=(´ο｀*)))唉!",self.bug_sad,screen)
            elif self.textNum==4:
                PDialog.show_dialog_player(self.dialogPlayer,"这，这可怎么办？",screen)
            elif self.textNum==5:
                PDialog.show_dialog_bug(self.dialogBug,"um......",self.bug_silence,screen)
            elif self.textNum==6:
                PDialog.show_dialog_bug(self.dialogBug,"我的数据库里有一句人类的谚语......",self.bug_normal,screen)
            elif self.textNum==7:
                PDialog.show_dialog_player(self.dialogPlayer,"「书（密码）到用时方恨少」？",screen)
            elif self.textNum==8:
                PDialog.show_dialog_bug(self.dialogBug,"是「车到山前必有路」！[○･｀Д´･ ○]",self.bug_angry,screen)
            elif self.textNum==9:
                PDialog.show_dialog_player(self.dialogPlayer,"对，对。至少还有网络可以连，已经很让我惊讶了。",screen)
            elif self.textNum==10:
                PDialog.show_dialog_bug(self.dialogBug,"总之，天很晚了——系统时间显示，现在是晚上八点。要不你先去休息吧？一路走到这里，你一定很累了。",self.bug_normal,screen)
            elif self.textNum==11:
                PDialog.show_dialog_bug(self.dialogBug,"晚安，Player。记得给电脑关机哦！",self.bug_happy,screen)
            
                










    def handle_mouse_button_down(self, event):

        if event.button == 1:
            if self.gameMode == 1:
                if self.dialogNum == 1:
                    self.textNum += 1
                elif self.dialogNum == 2:
                    self.textNum += 1
                print(self.textNum , self.dialogNum, self.gameMode)


            elif self.gameMode == 0:
                x, y = event.pos
                
                if self.appicon.is_clicked((x, y)):#回退bug很可能就出在这儿了，调用两次click...真的是吗
                    #print(999)
                    id= self.appicon.is_clicked((x, y))
                    #print(9999)
                    if self.appicon.selected_icon :
                        self.appicon.display_window = id
                        self.appicon.selected_icon = None
                    else:
                        self.appicon.selected_icon = id 
                        print(id,"App icon clicked!")
                
                pygame.display.flip()
                    # 这里可以添加点击图标后的逻辑，比如打开一个新的窗口或执行某个操作

    def handle_mouse_motion(self, event):#不知道有啥用其实。
        x, y = event.pos


    def handle_keydown(self, event):
        if event.key == pygame.K_DOWN:
            self.gameMode = 0

    def update(self):
        super().update()
        self.transition_over=self.transition.update()
        if self.isopen and not self.transition.is_active():
                self.transition.start(duration=500)
        if self.transition_over:
            self.isopen=False
            self.transition_over=False
        if self.textNum >= 9 and self.dialogNum == 1:
            print("dialog1 over")
            self.textNum = 0
            self.dialogNum = 2
        if self.textNum >= 41 and self.dialogNum == 2:
            print("dialog2 over")
            self.textNum = 0
            self.dialogNum = 0
            self.gameMode = 0

            



    def draw(self):

 
        self.screen.blit(self.bgside, (0, 0))
        self.screen.blit(self.bg, (200, 0))

        self.screen.blit(self.bug_normal, (700, 700))  

        
        if self.gameMode==1:
            self.dialog(self.screen)


        x, y = pygame.mouse.get_pos()
        self.screen.blit(self.mouse, (x - 4, y - 4))

        self.appicon.draw_icon(self.screen)  # 绘制应用图标
        self.appicon.draw_window(self.screen)

        if self.isopen:
            self.transition.draw(0, 1, self.screen)


        self.screen.blit(self.screen_black, (0, 0))

