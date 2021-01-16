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
import pytesseract
from baidu import *
import threading

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

    def summon(self, index):
        self.reflesh()
        mouse.slide(self.hand_card_pos[index][0], self.hand_card_pos[index][1], 'up')
        mouse.click(BUTTON1[0], BUTTON1[1])
        cancle(3)
        tick(3)
        self.hand_card_num -= 1
    
    def magic(self, index, target = None):
        self.reflesh()
        mouse.slide(self.hand_card_pos[index][0], self.hand_card_pos[index][1], 'up')
        mouse.click(BUTTON1[0], BUTTON1[1])
        tick(2)
        if target:
            mouse.click(EFFECT_BUTTON[target][0], EFFECT_BUTTON[target][1])
        cancle(3)
        tick(3)
        self.hand_card_num -= 1
    
    def set_spell(self, index): 
        self.reflesh()
        mouse.slide(self.hand_card_pos[index][0], self.hand_card_pos[index][1], 'up')
        mouse.click(BUTTON2[0], BUTTON2[1])
        mouse.click(BUTTON3[0], BUTTON3[1])
        cancle(3)
        tick(3)
        self.hand_card_num -= 1

    def change_phase(self):
        mouse.click(TURN[0], TURN[1])
        mouse.click(TURN[0], TURN[1])
        cancle()
        tick(3)

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
            tick(6)

    def draw(self):
        mouse.click(DRAW[0], DRAW[1])
        mouse.click(DRAW[0], DRAW[1])
        cancle()
        tick(3)
    
    def reflesh(self):
        self.hand_card_pos = eval('HAND_CARD_' + self.hand_card_num)

duel = Duel()

class Analyze(object):
    def __init__(self):
        self.hwnd = mouse.handle
        self.hdc = win32gui.GetWindowDC(mouse.handle) #返回句柄窗口的设备环境，覆盖整个窗口，包括非客户区，标题栏，菜单，边框
        self.picpath = os.path.join('temp.bmp')
        self.check_hand_picpath = os.path.join('pic', 'handcard.bmp')
        self.img = None
        self.online_ocr = BaiduOCR(APP_KEY, SECRET_KEY)
    
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

    def point_color(self, point, deta = 1):
        point = [point[0] + 1, point[1] + 34]
        pixdata = self.img.load()
        rgb_s = pixdata[point[0], point[1]]
        for x in [deta, -deta]: 
            for y in [deta, -deta]:
                t = pixdata[point[0] + x, point[1] + y]
                rgb_s = [rgb_s[0] + t[0], rgb_s[1] + t[1], rgb_s[2] + t[2]]
        # s = ''
        # for i in rgb_s:
        #     s += hex(int(i / 5))[2:]
        # return s
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
        return result
    
    def pic_compare(self, im1, im2, acc = 20):
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
        # 阀值设为20
        return match < acc
    
    def check_handcard_num(self, num = 5): # num 是期望的手牌数量，不超过5
        crop_box = (32, 114, 523, 833)
        for i in range(len(CHECK_HANDCARD) - num, len(CHECK_HANDCARD)):
            mouse.buttondown(CHECK_HANDCARD[i][0], CHECK_HANDCARD[i][1])
            tick(1)
            self.shot()
            tick(1)
            mouse.buttonup(CHECK_HANDCARD[i][0], CHECK_HANDCARD[i][1])
            im1 = self.img.crop(crop_box)
            im2 = Image.open(self.check_hand_picpath)
            if self.pic_compare(im1, im2, 160):
                return len(CHECK_HANDCARD) - i
    
    def check_turn(self): # 多线程
        while True:
            img = self.shot('check.bmp')
            cropbox = (300, 84, 480, 112)
            # cropbox2 = (414, 43, 461, 80)
            im1 = img.crop(cropbox).convert('L')
            # im2 = img.crop(cropbox2).convert('L')
            # pixdata = im2.load()
            # for y in range(im2.size[1]): # 图片二值化
            #     for x in range(im2.size[0]):
            #         if pixdata[x, y] < 200:
            #             pixdata[x, y] = 0
            #         else:
            #             pixdata[x, y] = 255
            duel.phase = pytesseract.image_to_string(im1, lang = 'chi_sim')
            # duel.turn = self.online_ocr.read(im2, lang = 'ENG')
            print(duel.phase)
            del_file('check.bmp')
            tick(5)

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
        # im1.save('1.jpg')
        return self.online_ocr.read(im1)
    
    def monster(self):
        monster_fri_list = self.check_ground_card(MONSTER_F)
        monster_ene_list = self.check_ground_card(MONSTER_E)
        return monster_fri_list, monster_ene_list
    
    def check_ground_card(self, point_list):
        rgb_detail_check = (0, 212, 249)
        result = []
        for point in point_list:
            mouse.click(point[0], point[1])
            self.shot()
            rgb = self.point_color(DETAIL_CHECK, deta = 0)
            result.append(self.rgb_compare(rgb, rgb_detail_check, 10))
        return result



    
    # def show(self):
    #     self.shot()
    #     self.img = self.img.convert('L')
    #     self.img.show()

            
            

    
        
        

analyze = Analyze()

### 常用函数
def cancle(n = 1):
    for i in range(n): 
        mouse.click(CANCLE[0], CANCLE[1])
        tick()

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
    mouse.click(DUEL_START[0], DUEL_START[1])
    tick(4)
    mouse.click(DUEL_START[0], DUEL_START[1])
    mouse.click(DUEL_START[0], DUEL_START[1])
    tick(15)
    cancle(5)
    tsk = threading.Thread(target = analyze.check_turn, args = (), daemon = True)
    tsk.start()
    while True:
        if '你' in duel.phase:
            normal_summon = False 
            if '抽牌' in duel.phase :
                duel.draw()
            elif '主要' in duel.phase:
                duel.hand_card_num = analyze.check_handcard_num()
                duel.hand_card = analyze.hand_card(eval('HAND_CARD_' + str(duel.hand_card_num)))
                if not normal_summon:    
                    for index in range(len(duel.hand_card)):
                        if 'monster' in duel.hand_card[index]:
                            duel.summon(index)
                            del duel.hand_card[index]
                            normal_summon = True
                duel.spell_area = analyze.check_ground_card(SPELL_F)
                duel.monster_fri = analyze.check_ground_card(MONSTER_F)
                duel.monster_ene = analyze.check_ground_card(MONSTER_E)
                while duel.spell_area.count(True) < 3 and duel.hand_card.count('trap') + duel.hand_card.count('magic') > 0: 
                    for index in range(len(duel.hand_card)):
                        if duel.monster_fri.count(True):
                            if 'magic' in duel.hand_card[index]:
                                duel.magic(index, target = 0)
                                del duel.hand_card[index]
                            elif 'trap' in duel.hand_card[index]: 
                                duel.set_spell(index)
                                del duel.hand_card[index]
                        else:
                            if 'trap' in duel.hand_card[index]: 
                                duel.set_spell(index)
                                del duel.hand_card[index]
                    duel.spell_area = analyze.check_ground_card(SPELL_F)
                    if not 'magic' in duel.hand_card and not 'trap' in duel.hand_card: 
                        break
                duel.change_phase()
            elif '战斗' in duel.phase:
                for index in [1, 2, 0]:
                    if duel.monster_fri[index]:
                        target = None
                        for index2 in [1, 2, 0]:
                            if duel.monster_ene[index2]:
                                target = index2
                                break
                        duel.attack(index, target)
                duel.change_phase()
        elif '对手' in duel.phase:
            tick(2)
        else:
            print('决斗结束！')
                    
                    




                    

            


    # get_color()

    # duel.summon()
    # mouse.get_curse()
    # duel.change_phase()
    # duel.attack(2, 1)
    # duel.attack(1, 1)
    # duel.summon()
    # duel.battle_phase()
    # mouse.click(132, 508)
    # tick(5)
    
    # analyze.shot()
    # print(analyze.point_color(HAND_CARD_4[i]))
    # for i in range(4):
    #     print(analyze.point_color(HAND_CARD_4[i]))
    # print(analyze.point_color((427, 58)))
    # print(win32gui.GetWindowRect(mouse.handle))
    # duel.summon()
    # analyze.shot()
    # print(win32gui.GetWindowRect(mouse.parent_handle))
    # print(analyze.hand_card(HAND_CARD_4))
    # print(analyze.check_handcard_num())
    # tick(5)
    # analyze.shot()
    # img2 = analyze.img.crop((32, 114, 523, 833))
    # img2 = img2.convert('L')
    # img2.save('handcard.bmp')
    # analyze.judge_turn()
    # print(analyze.judge_card())
    # print(analyze.monster())
    # duel.change_phase()
    # duel.attack(1, None)

if __name__ == '__main__':
    main()