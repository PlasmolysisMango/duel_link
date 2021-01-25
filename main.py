import win32gui
import win32api
import win32con
import time
import os
import win32ui
from ctypes import windll
import operator
from constant import *
from PIL import Image
from baidu import *
from api_account import *

# 类定义以及初始实例化
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
    
    def double_click(self, cx, cy, hwnd = None):
        if not hwnd: 
            hwnd = self.handle
        long_position = win32api.MAKELONG(cx, cy)# 模拟鼠标指针 传送到指定坐标
        win32api.SendMessage(hwnd, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, long_position) # 模拟鼠标按下
        win32api.SendMessage(hwnd, win32con.WM_LBUTTONUP, win32con.MK_LBUTTON, long_position) # 模拟鼠标弹起
        tick(0.1)
        win32api.SendMessage(hwnd, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, long_position) # 模拟鼠标按下
        win32api.SendMessage(hwnd, win32con.WM_LBUTTONUP, win32con.MK_LBUTTON, long_position) # 模拟鼠标弹起
        tick()
    
    def buttondown(self, cx, cy, hwnd = None):
        if not hwnd: 
            hwnd = self.handle
        long_position = win32api.MAKELONG(cx, cy)# 模拟鼠标指针 传送到指定坐标
        win32api.SendMessage(hwnd, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, long_position) # 模拟鼠标按下
    
    def buttonup(self, cx, cy, hwnd = None):
        if not hwnd: 
            hwnd = self.handle
        long_position = win32api.MAKELONG(cx, cy)# 模拟鼠标指针 传送到指定坐标
        win32api.SendMessage(hwnd, win32con.WM_LBUTTONUP, win32con.MK_LBUTTON, long_position) # 模拟鼠标弹起
        
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
        windowRec = win32gui.GetWindowRect(self.handle)
        windowRec2 = win32gui.GetWindowRect(self.parent_handle)
        while True:
            tempt = win32api.GetCursorPos() # 记录鼠标所处位置的坐标
            x = tempt[0]-windowRec[0] # 计算相对x坐标
            y = tempt[1]-windowRec[1] # 计算相对y坐标
            x2 = tempt[0]-windowRec2[0] # 计算相对x坐标
            y2 = tempt[1]-windowRec2[1] # 计算相对y坐标
            print("子窗口：{}，{} / 父窗口：{}，{}".format(x, y, x2, y2))
            time.sleep(1) # 每0.5s输出一次
    
    def get_curse_test(self):
        windowRec = win32gui.GetWindowRect(self.handle)
        windowRec2 = win32gui.GetWindowRect(self.parent_handle)
        tempt = win32api.GetCursorPos() # 记录鼠标所处位置的坐标
        x = tempt[0]-windowRec[0] # 计算相对x坐标
        y = tempt[1]-windowRec[1] # 计算相对y坐标
        x2 = tempt[0]-windowRec2[0] # 计算相对x坐标
        y2 = tempt[1]-windowRec2[1] # 计算相对y坐标
        return x, y, x2, y2

mouse = Mouse() # 实例化鼠标对象

class Duel(object):
    def __init__(self):
        self.monster_fri = []
        self.monster_ene = []
        self.spell_fri = []
        self.hand_card = []
        self.hand_card_num = None
        self.hand_card_pos = []
        self.phase = None
        self.turn = 0
        self.chain = False

    def summon(self, index, delay = 2):
        self.reflesh()
        mouse.slide(self.hand_card_pos[index][0], self.hand_card_pos[index][1], 'up')
        mouse.click(BUTTON1[0], BUTTON1[1])
        if delay:
            cancle(delay)
            tick(delay)
        self.hand_card_num -= 1
    
    def magic(self, index, target = None):
        self.reflesh()
        mouse.slide(self.hand_card_pos[index][0], self.hand_card_pos[index][1], 'up')
        mouse.click(BUTTON1[0], BUTTON1[1])
        if target != None:
            cancle(2)
            tick(3)
            mouse.click(EFFECT_SELECT[target][0], EFFECT_SELECT[target][1])
            mouse.click(EFFECT_CONFIRM[0], EFFECT_CONFIRM[1])
        cancle(2)
        tick(2)
        self.hand_card_num -= 1
    
    def set_spell(self, index): 
        self.reflesh()
        mouse.slide(self.hand_card_pos[index][0], self.hand_card_pos[index][1], 'up')
        # mouse.click(BUTTON2[0], BUTTON2[1])
        mouse.click(BUTTON3[0], BUTTON3[1])
        cancle(2)
        tick(2)
        self.hand_card_num -= 1

    def change_phase(self):
        mouse.click(TURN[0], TURN[1])
        mouse.click(TURN[0], TURN[1])
        cancle()
        self.phase_flow()
        tick(3)
    
    def phase_flow(self):
        phase_list = ['你的抽卡阶段', '你的准备阶段', '你的主要阶段', '你的战斗阶段', 
        '你的结束阶段', '对手的抽卡阶段', '对手的准备阶段', '对手的主要阶段', 
        '对手的战斗阶段', '对手的结束阶段' ]
        if self.phase in phase_list:
            num = phase_list.index(self.phase)
            if num == len(phase_list) - 1:
                num = 0
            else:
                num += 1
            self.phase = phase_list[num]

    def attack(self, index1, index2):
        if index2 == None:
            lis = [1, 2, 0]
        else:
            lis = [index2]
        for index2 in lis:
            if index1 == index2: 
                pos = 'up'
            else:
                pos = MONSTER_E[index2]
            mouse.slide(MONSTER_F[index1][0], MONSTER_F[index1][1], pos)
            cancle()
            tick(3)
        cancle(2)

    def draw(self):
        mouse.click(DRAW[0], DRAW[1])
        mouse.click(DRAW[0], DRAW[1])
        cancle()
        tick(3)
    
    def reflesh(self):
        self.hand_card_pos = eval('HAND_CARD_' + str(self.hand_card_num))
        n = 5 - self.hand_card_num
        mouse.click(CHECK_HANDCARD[n][0], CHECK_HANDCARD[n][1])

duel = Duel()

class Analyze(object):
    def __init__(self):
        self.hwnd = mouse.handle
        self.hdc = win32gui.GetWindowDC(mouse.handle) #返回句柄窗口的设备环境，覆盖整个窗口，包括非客户区，标题栏，菜单，边框
        self.picpath = os.path.join('temp.bmp')
        self.img = None
        self.online_ocr = BaiduOCR(APP_KEY, SECRET_KEY)
        self.routine = True
        self.next = False
        self.recent_chain = False
    
    def shot(self, filename = None):
        hdc = win32gui.GetWindowDC(mouse.parent_handle)
        left, top, right, bot = win32gui.GetWindowRect(mouse.parent_handle) #获取句柄窗口的大小信息
        width = right - left
        height = bot - top
        mfcDC = win32ui.CreateDCFromHandle(hdc) #创建设备描述表
        saveDC = mfcDC.CreateCompatibleDC() #创建内存设备描述表
        saveBitMap = win32ui.CreateBitmap() #创建位图对象准备保存图片
        saveBitMap.CreateCompatibleBitmap(mfcDC,width,height) #为bitmap开辟存储空间
        saveDC.SelectObject(saveBitMap) #将截图保存到saveBitMap中
        saveDC.BitBlt((0,0), (width,height), mfcDC, (0, 0), win32con.SRCCOPY) #保存bitmap到内存设备描述表
        #如果要截图到打印设备：
        ###最后一个int参数：0-保存整个窗口，1-只保存客户区。如果PrintWindow成功函数返回值为1
        result = windll.user32.PrintWindow(mouse.parent_handle, saveDC.GetSafeHdc(), 0)
        if not filename:
            filename = "temp.bmp"
        saveBitMap.SaveBitmapFile(saveDC, filename) # 保存bitmap到文件
        if filename == "temp.bmp":
            self.img = Image.open(self.picpath)
            self.img = self.img.convert('RGB')
        else:
            img = Image.open(filename)
            return img

    def point_color(self, point, deta = 1, img = None):
        point = [point[0] + 1, point[1] + 34]
        if not img: 
            img = self.img
        pixdata = img.load()
        rgb_s = pixdata[point[0], point[1]]
        for x in [deta, -deta]: 
            for y in [deta, -deta]:
                t = pixdata[point[0] + x, point[1] + y]
                rgb_s = [rgb_s[0] + t[0], rgb_s[1] + t[1], rgb_s[2] + t[2]]
        return (int(rgb_s[0] / 5), int(rgb_s[1] / 5), int(rgb_s[2] / 5))
    
    def rgb_compare(self, rgb, rgb_c, acc = 30):
        r, g, b = rgb[0], rgb[1], rgb[2]
        r_c, g_c, b_c = rgb_c[0], rgb_c[1], rgb_c[2]
        if r_c - acc < r < r_c + acc: 
            if g_c - acc < g < g_c + acc: 
                if b_c - acc < b < b_c + acc: 
                    return True
        return False

    def hand_card(self, hand_card_list):
        self.shot()
        result = []
        rgb_effect_monster = (188, 110, 63)
        rgb_normal_monster = (194, 154, 81)
        rgb_trap = (180, 45, 125)
        rgb_magic = (0, 139, 118)
        for point_index in range(len(hand_card_list)):
            rgb = self.point_color(hand_card_list[point_index])
            if self.rgb_compare(rgb, rgb_normal_monster):
                result.append('normal_monster')
            elif self.rgb_compare(rgb, rgb_effect_monster):
                result.append('effect_monster')
            elif self.rgb_compare(rgb, rgb_trap):
                result.append('trap')
            elif self.rgb_compare(rgb, rgb_magic):
                result.append('magic')
            else:
                result.append('unknown')
        del_file('temp.bmp')

        return result
    
    def pic_compare(self, im1, im2, acc = 30, show = False):
        # 缩小图标，转成灰度
        image1 = im1.resize((20, 20), Image.ANTIALIAS).convert("L")
        image2 = im2.resize((20, 20), Image.ANTIALIAS).convert("L")
        # 将灰度图标转成01串,即系二进制数据
        pixels1 = list(image1.getdata())
        pixels2 = list(image2.getdata())
        avg1 = sum(pixels1) / len(pixels1)
        avg2 = sum(pixels2) / len(pixels2)
        hash1 = "".join(map(lambda p: "1" if p > avg1 else "0", pixels1))
        hash2 = "".join(map(lambda p: "1" if p > avg2 else "0", pixels2))
        # 统计两个01串不同数字的个数
        match = sum(map(operator.ne, hash1, hash2))
        if show:
            print('识别阈值{}'.format(match))
        # acc为识别阈值
        return match < acc
    
    def check_handcard_num(self, num = 5): # num 是期望的手牌数量，不超过5
        crop_box = (32, 114, 523, 833)
        for i in range(len(CHECK_HANDCARD) - num, len(CHECK_HANDCARD)):
            mouse.buttondown(CHECK_HANDCARD[i][0], CHECK_HANDCARD[i][1])
            tick(1)
            img = self.shot('hand_card.bmp')
            tick(1)
            mouse.buttonup(CHECK_HANDCARD[i][0], CHECK_HANDCARD[i][1])
            rgb_c = (45, 47, 72)
            rgb = (0, 0, 0)
            for point in HAND_CARD_NUM_CHECK_POINT:
                rgb = list_add(rgb, self.point_color(point, img = img, deta = 0))
            rgb = list_div(rgb, len(HAND_CARD_NUM_CHECK_POINT))
            del_file('hand_card.bmp')
            if self.rgb_compare(rgb, rgb_c):
                return len(CHECK_HANDCARD) - i
            # else:
            #     print(rgb)
    
    def routine_check(self, mode = 'phase'):
        img = self.shot('check.bmp')

        if 'phase' in mode: 
            # cropbox = (300, 84, 480, 112)
            # im1 = img.crop(cropbox).convert('L')
            # duel.phase = self.online_ocr.read(im1)s

            crop_box = (284, 83, 479, 110)
            img_phase = img.crop(crop_box)
            for phase_file in os.listdir('phase'):
                img_c = Image.open(os.path.join('phase', phase_file))
                if self.pic_compare(img_phase, img_c, 15): 
                    duel.phase = phase_file[:-4]
                    break
        
        if 'chain' in mode: 
            self.recent_chain = False
            while True:
                cancle()
                rgb_chain = (255, 255, 255)
                rgb = self.point_list_color(CHAIN_CHECK_POINT, img)
                chain = self.rgb_compare(rgb, rgb_chain, 20)
                if chain:
                    self.recent_chain = True 
                    if '对手' in duel.phase: 
                        mouse.click(CHAIN_SELECT[0][0], CHAIN_SELECT[0][1])
                        mouse.click(CHAIN_CONFRIM[0], CHAIN_CONFRIM[1])
                        cancle()
                        tick(3)
                        mouse.click(EFFECT_SELECT[0][0], EFFECT_SELECT[0][1])
                        mouse.click(EFFECT_CONFIRM[0], EFFECT_CONFIRM[1])
                    else:
                        mouse.click(CHAIN_CANCEL[0], CHAIN_CANCEL[1])
                    cancle()
                    img = self.shot('check.bmp')
                else:
                    break
        
        if mode:
            rgb_end = (47, 120, 2)
            if self.rgb_compare(self.point_color(END_CHECK, img = img), rgb_end, 10):
                duel.phase = '决斗结束'
        
        if 'next' in mode:
            self.next = False
            cropbox_next = (22, 949, 158, 1023)
            im_next = img.crop(cropbox_next).convert('L')
            im_next_c = Image.open(os.path.join('pic', 'next.bmp'))
            self.next = self.pic_compare(im_next, im_next_c, 50)

        del_file('check.bmp')

    def judge_card(self):
        self.shot()
        cropbox = (32, 265, 400, 294)
        im1 = self.img.crop(cropbox).convert('L')
        pixdata = im1.load()
        for y in range(im1.size[1]): # 图片二值化
            for x in range(im1.size[0]):
                if pixdata[x, y] < 200:
                    pixdata[x, y] = 255
                else:
                    pixdata[x, y] = 0
        del_file('temp.bmp')
        return self.online_ocr.read(im1)
    
    def check_ground_card(self, point_list):
        result = []
        for point in point_list:
            res = self.card_exist(point)
            if res:
                cancle()
            result.append(res)
        return result
    
    def target_card(self, point_list, mode = True, order = [1, 2, 0]): # 用于返回第一个存在的目标
        for index in order:
            res = self.card_exist(point_list[index])
            if res == mode:
                return index
        return None
    
    def card_exist(self, card_point):
        rgb_detail_check = (0, 212, 249)
        mouse.click(card_point[0], card_point[1])
        img = self.shot('c_exist.bmp')
        rgb = self.point_color(DETAIL_CHECK, deta = 0, img = img)
        del_file('c_exist.bmp')
        return self.rgb_compare(rgb, rgb_detail_check, 10)
    
    def point_list_color(self, point_list, img):
        rgb = (0, 0, 0)
        for point in point_list:
            rgb = list_add(rgb, self.point_color(point, img = img, deta = 0))
        rgb = list_div(rgb, len(point_list))
        return rgb



analyze = Analyze()

### 常用函数
def cancle(n = 1):
    for i in range(n): 
        mouse.double_click(CANCLE[0], CANCLE[1])

def tick(n = 1):
    time.sleep(n)

def get_color():
    while 1: 
        x, y, x2, y2 = mouse.get_curse_test()
        analyze.shot()
        print((x, y), (x2, y2), analyze.point_color((x, y)))
        tick(1)

def list_add(lis1, lis2):
    lis = []
    if len(lis1) == len(lis2): 
        for i in range(len(lis1)):
            lis.append(lis1[i] + lis2[i])
        return lis

def list_div(lis, n):
    lis2 = []
    for i in range(len(lis)):
        lis2.append(int(lis[i] / n))
    return lis2

def del_file(filename):
    if os.path.exists(filename):
        os.remove(filename)


def main():
    duel_start = True
    duel_num = 1
    while True:
        if duel_start:
            print('----第{}局----'.format(duel_num))
            mouse.click(PORT[0], PORT[1])
            tick(2)
            mouse.click(DUEL_START[0], DUEL_START[1])
            tick(2)
            mouse.click(DUEL_CONFIRM[0], DUEL_CONFIRM[1])
            mouse.click(DUEL_START[0], DUEL_START[1])
            mouse.click(DUEL_START[0], DUEL_START[1])
            tick(15)
            cancle(5)
            while True:
                analyze.routine_check()
                if '阶段' in duel.phase:
                    break
                tick(2)
            duel_start = False
        if '你' in duel.phase:
            normal_summon = False 
            if '抽卡' in duel.phase :
                print(duel.phase)
                duel.draw()
                duel.phase_flow()
            elif '准备' in duel.phase:
                print(duel.phase)
                duel.phase_flow()
            elif '主要' in duel.phase:
                print(duel.phase)
                print('确认手牌数量...')
                duel.hand_card_num = analyze.check_handcard_num()
                print('手牌数量：{}'.format(duel.hand_card_num))
                tick(2)
                duel.hand_card = analyze.hand_card(eval('HAND_CARD_' + str(duel.hand_card_num)))
                print('分析手牌：{}'.format(duel.hand_card))
                print('检查怪兽数量...')
                duel.monster_fri = analyze.check_ground_card(MONSTER_F)
                if not normal_summon and duel.monster_fri.count(True) < 3:    
                    for index in range(len(duel.hand_card)):
                        if 'monster' in duel.hand_card[index]:
                            print('召唤怪兽')
                            duel.summon(index)
                            del duel.hand_card[index]
                            normal_summon = True
                            for index in [1, 2, 0]:
                                if not duel.monster_fri[index]:
                                    duel.monster_fri[index] = True
                                    break
                            break
                analyze.routine_check('chain')
                if '决斗结束' in duel.phase:
                    continue
                print('检查战场状况...')
                if analyze.recent_chain:
                    duel.monster_fri = analyze.check_ground_card(MONSTER_F)
                while duel.hand_card.count('trap') + duel.hand_card.count('magic') > 0: 
                    duel.spell_fri = analyze.check_ground_card(SPELL_F)
                    if duel.spell_fri.count(True) > 2 or not duel.monster_fri.count(True):
                        break
                    print('开始使用魔法陷阱')
                    for index in range(len(duel.hand_card)):
                        if 'magic' in duel.hand_card[index]:
                            print('我方有怪兽，使用魔法卡')
                            duel.magic(index, target = 0)
                            del duel.hand_card[index]
                            break
                        elif 'trap' in duel.hand_card[index]:
                            print('盖放陷阱卡')
                            duel.set_spell(index)
                            del duel.hand_card[index]
                            break
                    analyze.routine_check('chain')
                    if '决斗结束' in duel.phase:
                        break
                duel.change_phase()
                analyze.routine_check('phase, chain')
            elif '战斗' in duel.phase:
                print(duel.phase)
                print('检查战场状况')
                for index in [1, 2, 0]:
                    if duel.monster_fri[index]:
                        target = analyze.target_card(MONSTER_E)
                        print('攻击：【{}】->【{}】'.format(index, target))
                        duel.attack(index, target)
                        tick(1)
                        analyze.routine_check('chain, end')
                        if '决斗结束' in duel.phase:
                            break
                duel.change_phase()
            elif '结束阶段' in duel.phase:
                duel.phase_flow()
        elif '对手' in duel.phase:
            analyze.routine_check('phase, chain')
            print(duel.phase)
            tick()
        elif '决斗结束' in duel.phase:
            print('决斗结束！')
            while not analyze.next:
                mouse.click(END_BUTTON[0], END_BUTTON[1])
                tick(2)
                analyze.routine_check('next')
                if analyze.next:
                    tick()
                    analyze.routine_check('next')
            duel_start = True
            analyze.next = False
            duel_num += 1

if __name__ == '__main__':
    main()