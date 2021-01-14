import win32gui
import win32api
import win32con
import time

DUEL_START = (283, 894) # 决斗开始按钮
HAND_CARD_X = (90, 150, 210, 270, 340) # 手牌的x坐标
HAND_CARD_Y = 960 # 手牌的y坐标
CANCLE = (50, 50) # 取消
TURN = (517, 661) # 回合结束按钮1
TURN2 = (517, 506) # 回合结束按钮2
BUTTON1 = (214, 765) # 按钮1：召唤
BUTTON2 = (345, 765) # 按钮2：覆盖
MONSTER_X = (185, 295, 405) # 怪兽位置X坐标
MONSTER_Y = 585 # 怪兽位置Y坐标
DRAW = (295, 585) # 抽卡坐标

class Mouse(object):
    def __init__(self):
        self.parent_handle = win32gui.FindWindow(0, '雷电模拟器')
        self.handle = win32gui.FindWindowEx(self.parent_handle, 0, 'RenderWindow', None)

    def click(self, cx, cy, hwnd = None): # 窗口内的相对坐标
        if not hwnd: 
            hwnd = self.handle
        long_position = win32api.MAKELONG(cx, cy)# 模拟鼠标指针 传送到指定坐标
        win32api.SendMessage(hwnd, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, long_position) # 模拟鼠标按下
        win32api.SendMessage(hwnd, win32con.WM_LBUTTONUP, win32con.MK_LBUTTON, long_position) # 模拟鼠标弹起
        tick()
    
    def slide(self, cx1, cy1, pos, hwnd = None):
        if not hwnd: 
            hwnd = self.handle
        if pos == 'up':
            cx2 = cx1
            cy2 = cy1 - 200
        elif pos == 'down':
            cx2 = cx1
            cy2 = cy1 + 200
        elif pos == 'right': 
            cx2 = cx1 + 200
            cy2 = cy1
        elif pos == 'left': 
            cx2= cx1 - 200
            cy2 = cy1
        else:
            cx2 = pos[0]
            cy2 = pos[1]
        long_position1 = win32api.MAKELONG(cx1, cy1)
        long_position2 = win32api.MAKELONG(cx2, cy2)
        win32api.SendMessage(hwnd, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, long_position1) # 模拟鼠标按下
        time.sleep(0.5)
        win32api.SendMessage(hwnd, win32con.WM_MOUSEMOVE, win32con.MK_LBUTTON, long_position2)   # 移动到终点
        time.sleep(0.5)
        win32api.SendMessage(hwnd, win32con.WM_LBUTTONUP, win32con.MK_LBUTTON, long_position2) # 模拟鼠标弹起
        tick()

    def get_curse(self):
        windowRec = win32gui.GetWindowRect(self.parent_handle)
        while True:
            tempt = win32api.GetCursorPos() # 记录鼠标所处位置的坐标
            x = tempt[0]-windowRec[0] # 计算相对x坐标
            y = tempt[1]-windowRec[1] # 计算相对y坐标
            print(x,y)
            time.sleep(0.5) # 每0.5s输出一次

mouse = Mouse() # 实例化鼠标对象

class Duel(object):
    def __init__(self):
        self.monster = [0]
        self.magic = []
        self.trap = []

    def summon(self):
        index = self.monster[0]
        mouse.slide(HAND_CARD_X[index], HAND_CARD_Y, 'up')
        mouse.click(BUTTON1[0], BUTTON1[1])
        cancle()
        tick(3)

    def change_phase(self):
        mouse.click(TURN[0], TURN[1])
        mouse.click(TURN[0], TURN[1])
        cancle()
        tick(3)

    def attack(self, index1, index2):
        if index1 == index2: 
            pos = 'up'
        else:
            pos = MONSTER_X[index2], MONSTER_Y - 200
        mouse.slide(MONSTER_X[index1], MONSTER_Y, pos)
        cancle()
        tick(6)

    def draw(self):
        mouse.slide(DRAW[0], DRAW[1], 'down')
        cancle()
        tick(3)

duel = Duel()

def cancle():
    mouse.click(CANCLE[0], CANCLE[1])
    tick()

def tick(n = 1):
    time.sleep(0.5 * n)

def main():
    # mouse.click(DUEL_START[0], DUEL_START[1])
    # mouse.get_curse()
    # duel.attack(1, 1)
    # duel.summon()
    # duel.change_phase()
    # duel.attack(2, 1)
    # duel.attack(1, 1)
    # duel.summon()
    # duel.battle_phase()

if __name__ == '__main__':
    main()