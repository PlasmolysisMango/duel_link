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
        self.phase = ''
        self.turn = 0
        self.chain = False

    def summon(self, index, delay = 1):
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
            cancle(1)
            tick(1)
            mouse.click(EFFECT_SELECT[target][0], EFFECT_SELECT[target][1])
            mouse.click(EFFECT_CONFIRM[0], EFFECT_CONFIRM[1])
        cancle(1)
        tick(1)
        self.hand_card_num -= 1
    
    def set_spell(self, index): 
        self.reflesh()
        mouse.slide(self.hand_card_pos[index][0], self.hand_card_pos[index][1], 'up')
        mouse.click(BUTTON3[0], BUTTON3[1])
        cancle(1)
        tick(1)
        self.hand_card_num -= 1

    def change_phase(self):
        mouse.click(TURN[0], TURN[1])
        mouse.click(TURN[0], TURN[1])
        self.phase_flow()
        tick(1)
    
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
            lis = [1]
        else:
            lis = [index2]
        for index2 in lis:
            if index1 == index2: 
                pos = 'up'
            else:
                pos = MONSTER_E[index2]
            mouse.slide(MONSTER_F[index1][0], MONSTER_F[index1][1], pos)
            cancle()
            tick(1)
        cancle(1)

    def draw(self):
        mouse.click(DRAW[0], DRAW[1])
        mouse.click(DRAW[0], DRAW[1])
        cancle()
        tick(1)
    
    def reflesh(self):
        self.hand_card_pos = eval('HAND_CARD_' + str(self.hand_card_num))
        n = len(CHECK_HANDCARD) - self.hand_card_num
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
        rgb_effect_monster = (188, 110, 63)
        rgb_normal_monster = (194, 154, 81)
        rgb_trap = (180, 45, 125)
        rgb_magic = (0, 139, 118)
        acc = 30
        oldres = None
        while True:
            img = self.shot('hand.bmp')
            result = []
            for point_index in range(len(hand_card_list)):
                rgb = self.point_color(hand_card_list[point_index], deta = 0, img = img)
                if self.rgb_compare(rgb, rgb_normal_monster, acc):
                    result.append('normal_monster')
                elif self.rgb_compare(rgb, rgb_effect_monster, acc):
                    result.append('effect_monster')
                elif self.rgb_compare(rgb, rgb_trap, acc):
                    result.append('trap')
                elif self.rgb_compare(rgb, rgb_magic, acc):
                    result.append('magic')
                else:
                    result.append('unknown')
            if 'unknown' in result:
                acc += 10
                if acc > 80:
                    print('识别精度低')
                else:
                    continue
            if oldres == result:
                break
            else:
                oldres = result  
        del_file('hand.bmp')
        return result
    
    def pic_compare(self, im1, im2, acc = 30, show = False):
        match = self.pic_compare_value(im1, im2)
        if show:
            print('识别阈值{}'.format(match))
        # acc为识别阈值
        return match < acc
    
    def pic_compare_value(self, im1, im2):
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
        return match
    
    def check_handcard_num(self, num = len(CHECK_HANDCARD)): # num 是期望的手牌数量，不超过5
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
    
    def routine_check(self, mode = 'phase'):
        ''' 用于检测切换阶段的关键参数
        
        :param mode:
                    'phase'：将当前阶段返回duel.phase
                    'chain': 检测当前是否存在连锁，若存在，则进行连锁操作。将结果返回analyze.recent_chain
                    'next': 检测是否满足进行下一局的条件，此条件可根据需要重写，将结果返回analyze.next
                    'chaintarget': 在处理连锁时还会处理效果目标选择
                    *** 所有mode均可同时使用，如'phase, chaintarget, next'
        :return None
        :raise_error None
        '''
        img = self.shot('check.bmp')

        if 'phase' in mode: 
            crop_box = (284, 83, 479, 110)
            img_phase = img.crop(crop_box)
            res_list = []
            phase_list = os.listdir('phase')
            for phase_file in phase_list:
                img_c = Image.open(os.path.join('phase', phase_file))
                res_list.append(self.pic_compare_value(img_phase, img_c))
            value = sorted(res_list)[0]
            if value < 100:
                phase_file = phase_list[res_list.index(value)]
                duel.phase = phase_file[:-4]

        
        if 'chain' in mode: 
            self.recent_chain = False
            while True:
                rgb_chain = (255, 255, 255)
                rgb = self.point_list_color(CHAIN_CHECK_POINT, img)
                chain = self.rgb_compare(rgb, rgb_chain, 20)
                if chain:
                    self.recent_chain = True 
                    if '对手' in duel.phase: 
                        mouse.click(CHAIN_SELECT[0][0], CHAIN_SELECT[0][1])
                        mouse.click(CHAIN_CONFRIM[0], CHAIN_CONFRIM[1])
                        if 'chaintarget' in mode:
                            cancle()
                            tick()
                            mouse.click(EFFECT_SELECT[0][0], EFFECT_SELECT[0][1])
                            mouse.click(EFFECT_CONFIRM[0], EFFECT_CONFIRM[1])
                    else:
                        mouse.click(CHAIN_CANCEL[0], CHAIN_CANCEL[1])
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
        ''' 用于检测当前点按的卡牌名称
        
        :param None
        :return str
        :raise_error None
        '''
        self.shot()
        cropbox = JUDGE_CARD_RECT
        im1 = self.img.crop(cropbox).convert('L')
        pixdata = im1.load()
        for y in range(im1.size[1]): # 图片二值化
            for x in range(im1.size[0]):
                if pixdata[x, y] < 200:
                    pixdata[x, y] = 255
                else:
                    pixdata[x, y] = 0
        res = self.online_ocr.read(im1)
        if not res:
            print('ERROR:未识别到卡片名称！')
            im1.save('error.jpg')
        del_file('temp.bmp')
        return res
    
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
    
    def check_deck_status(self):
        ''' 返回卡组的状态，False为空

        :param None
        :return bool:fri_deck_stat, bool:ene_deck_stat
        :raise_error None
        '''
        img = self.shot('deck.bmp')
        point_e = (80, 254)
        point_f = (509, 741)
        rgb_deck = (50, 10, 10)
        rgb_e = self.point_color(point_e, deta = 2, img = img)
        rgb_f = self.point_color(point_f, deta = 2, img = img)
        res_e = self.rgb_compare(rgb_e, rgb_deck, acc = 60)
        res_f = self.rgb_compare(rgb_f, rgb_deck, acc = 60)
        del_file('deck.bmp')
        if not res_e or not res_f:
            print('我方卡组RGB：{}，对方卡组RGB：{}'.format(rgb_f, rgb_e))
        return res_f, res_e
    
    def check_skill(self):
        ''' 检查技能的可用状态

        :param None
        :return bool:skill_status
        :raise_error None
        '''
        img = self.shot('skill.bmp')
        cropbox = (374, 276, 512, 331)
        im1 = img.crop(cropbox).convert('L')
        res = self.online_ocr.read(im1)
        del_file('skill.bmp')
        if '技能' in res:
            return True
        else:
            return False

analyze = Analyze()

class Routine(object):
    """ 决斗的流程，默认是刷门的最简单流程，可根据需要进行继承重写

    :param None
    :return None
    :raise error None
    """
    def __init__(self):
        self.duel_start = True
        self.duel_num = 1
        self.normal_summon = False
    
    def run(self):
        while True:
            if self.duel_start:
                print('----第{}局----'.format(self.duel_num))
                self.duel_start_act()
            if '你' in duel.phase:
                self.normal_summon = False
                if '抽卡' in duel.phase:
                    print(duel.phase)
                    self.draw_phase()
                    duel.phase_flow()
                elif '准备' in duel.phase:
                    print(duel.phase)
                    self.prepare_phase()
                    duel.phase_flow()
                elif '主要' in duel.phase:
                    print(duel.phase)
                    self.main_phase()
                    duel.change_phase()
                    analyze.routine_check('phase, chain')
                elif '战斗' in duel.phase:
                    print(duel.phase)
                    self.battle_phase()
                    duel.change_phase()               
                elif '结束阶段' in duel.phase:
                    print(duel.phase)
                    self.end_phase()
                    duel.phase_flow()
            elif '对手' in duel.phase:
                self.enemy_phase()
            elif '决斗结束' in duel.phase:
                print('决斗结束！')
                self.duel_end_act()
                self.duel_num += 1
                self.duel_start = True
                duel.hand_card_num = None

    def enemy_phase(self):
        analyze.routine_check('phase, chaintarget')
        print(duel.phase)
        time.sleep(0.5)

    def duel_start_act(self):
        mouse.click(PORT[0], PORT[1])
        tick(2)
        mouse.click(DUEL_START[0], DUEL_START[1])
        tick(2)
        mouse.click(DUEL_CONFIRM[0], DUEL_CONFIRM[1])
        mouse.click(DUEL_START[0], DUEL_START[1])
        mouse.click(DUEL_START[0], DUEL_START[1])
        tick(15)
        while True:
            analyze.routine_check()
            if '阶段' in duel.phase:
                break
            tick(2)
        self.duel_start = False

    def draw_phase(self):
        duel.draw()
        
    def prepare_phase(self):
        analyze.routine_check('chain')

    def main_phase(self):
        print('确认手牌数量...')
        if duel.hand_card_num:
            duel.reflesh()
            point = duel.hand_card_pos[duel.hand_card_num - 1]
            mouse.click(point[0],point[1]) 
        duel.hand_card_num = analyze.check_handcard_num()
        print('手牌数量：{}'.format(duel.hand_card_num))
        tick(2)
        duel.hand_card = analyze.hand_card(eval('HAND_CARD_' + str(duel.hand_card_num)))
        print('分析手牌：{}'.format(duel.hand_card))
        print('检查怪兽数量...')
        duel.monster_fri = analyze.check_ground_card(MONSTER_F)
        if not self.normal_summon and duel.monster_fri.count(True) < 3:    
            for index in range(len(duel.hand_card)):
                if 'monster' in duel.hand_card[index]:
                    print('召唤怪兽')
                    duel.summon(index)
                    del duel.hand_card[index]
                    self.normal_summon = True
                    for index in [1, 2, 0]:
                        if not duel.monster_fri[index]:
                            duel.monster_fri[index] = True
                            break
                    break
        analyze.routine_check('chain')
        if '决斗结束' in duel.phase:
            return
        if analyze.recent_chain:
            duel.monster_fri = analyze.check_ground_card(MONSTER_F)
        while duel.hand_card.count('trap') + duel.hand_card.count('magic') > 0: 
            print('检查魔陷数量...')
            duel.spell_fri = analyze.check_ground_card(SPELL_F)
            if duel.spell_fri.count(True) > 2 or not duel.monster_fri.count(True):
                break
            print('使用魔法陷阱')
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
        

    def battle_phase(self):
        for index in [1, 2, 0]:
            if duel.monster_fri[index]:
                target = analyze.target_card(MONSTER_E)
                print('攻击：【{}】->【{}】'.format(index, target))
                duel.attack(index, target)
                analyze.routine_check('chain, end')
                if '决斗结束' in duel.phase:
                    break
        analyze.routine_check('end')

    def end_phase(self):
        analyze.routine_check('phase, chain')

    def duel_end_act(self):
        while not analyze.next:
            mouse.click(END_BUTTON[0], END_BUTTON[1])
            tick(2)
            analyze.routine_check('next')
            if analyze.next:
                tick()
                analyze.routine_check('next')
        analyze.next = False

default = Routine()

class Mai(Routine):
    ''' 孔雀舞10级门的刷分流程，继承自Routine

    '''
    def __init__(self):
        super(Mai, self).__init__()
        self.card_list = []
        self.hand_check = True
        self.add_card = 1
        self.magic_monster = False
        self.magic_grant = False
        self.power = False
        self.final_turn = False
        self.attack = False
        self.ready_card = False
        self.deck_num = 20
        self.ready_num = 0

    def enemy_phase(self):
        analyze.routine_check('phase, chain')
        if analyze.recent_chain:
            self.add_card += 1
        print(duel.phase)
        time.sleep(0.5)

    def draw_phase(self):
        tick(1)
        mouse.click(SKILL[0], SKILL[1])
        mouse.click(SKILL_CONFIRM[0], SKILL_CONFIRM[1])
        duel.draw()
    
    def run(self):
        # duel.hand_card_num = None
        # self.add_card = 3
        # self.card_list = []
        # self.hand_check = False
        # self.magic_monster = True
        # self.duel_start = False
        # self.magic_grant = True
        # self.deck_num = 20
        # duel.phase = '你的主要阶段'
        super(Mai, self).run()

    def main_phase(self):
        print('确认手牌数量...')
        print('原手牌：{}，增加：{}'.format(duel.hand_card_num, self.add_card))
        
        if duel.hand_card_num != None:
            duel.hand_card_num += self.add_card
            duel.reflesh()
            # if duel.hand_card_num != 1:
            #     duel.reflesh()
            #     point = duel.hand_card_pos[duel.hand_card_num - 1]
            #     mouse.click(point[0],point[1])
        else:
            duel.hand_card_num = analyze.check_handcard_num()
        print('手牌数量：{}'.format(duel.hand_card_num))
        tick(2)
        duel.hand_card = analyze.hand_card(eval('HAND_CARD_' + str(duel.hand_card_num)))
        print('分析手牌：{}'.format(duel.hand_card))
        
        print('检查手牌名称...')
        duel.reflesh()
        cancle()
        if self.hand_check:
            for index in range(duel.hand_card_num):
                point = duel.hand_card_pos[index]
                mouse.click(point[0], point[1])
                tick()
                judge_card_name = analyze.judge_card()
                if judge_card_name: 
                    self.card_list.append(judge_card_name)
            self.hand_check = False
            self.deck_num -= duel.hand_card_num
        else:
            for i in range(self.add_card):
                if self.ready_card:
                    self.card_list.append('ready')
                    continue
                index = duel.hand_card_num - self.add_card + i
                point = duel.hand_card_pos[index]
                mouse.click(point[0], point[1])
                tick()
                judge_card_name = analyze.judge_card()
                if judge_card_name: 
                    self.card_list.append(judge_card_name)
            self.deck_num -= self.add_card
        self.add_card = 1
        if not self.ready_card:
            self.ready_num = 0
            for card in self.card_list:
                if '电子巨人' in card or '力量' in card or '继承之力' in card:
                    self.ready_num += 1
            if self.ready_num == 3:
                self.ready_card = True
        print('手牌构成：{}'.format(self.card_list))

        print('检查卡组状态...')
        cancle()
        tick()
        self.fri_deck_stat, self.ene_deck_stat = analyze.check_deck_status()
        if not self.fri_deck_stat or not self.ene_deck_stat:
            self.final_turn = True
        print('我方卡组状态：{}，对方卡组状态：{}\n我方卡组数量：{}'.
            format(self.fri_deck_stat, self.ene_deck_stat, self.deck_num))
        
        for index in range(len(self.card_list)):
            if ('兽' in self.card_list[index] and duel.hand_card.count('magic') > 
                self.card_list.count('力量') + self.card_list.count('继承之力')):
                print('召唤魔导兽')
                duel.summon(index)
                del duel.hand_card[index]
                del self.card_list[index]
                self.normal_summon = True
                self.magic_monster = True
                break
        if self.magic_monster:
            area = 3
            while True:
                for index in range(len(self.card_list)):
                    if 'magic' in duel.hand_card[index]:
                        if self.card_list[index] in ['力量', '继承之力']:
                            continue
                        elif '斧头' in self.card_list[index]:
                            area -= 1
                        print('使用魔法卡')
                        duel.magic(index, target = 0)
                        del duel.hand_card[index]
                        del self.card_list[index]
                        break
                if duel.hand_card.count('trap') >= self.deck_num:
                    break
                for index in range(len(self.card_list)):
                    if 'trap' in duel.hand_card[index]:
                        print('盖放陷阱卡')
                        area -= 1
                        duel.set_spell(index)
                        del duel.hand_card[index]
                        del self.card_list[index]
                        break
                if (duel.hand_card.count('magic') == 
                    self.card_list.count('力量') + self.card_list.count('继承之力')):
                    print('手牌魔法：{}'.format(duel.hand_card.count('magic')))
                    print('手牌力量+继承之力：{}'.format(self.card_list.count('力量') + self.card_list.count('继承之力')))
                    break
                if area == 0:
                    print('无魔法陷阱区域')
                    break
        if self.final_turn:
            while True:
                for index in range(len(self.card_list)):
                    if '电子巨人' in self.card_list[index]:
                        print('召唤魔导电子巨人')
                        duel.reflesh()
                        point = duel.hand_card_pos[index]
                        mouse.slide(point[0], point[1], 'up')
                        mouse.click(BUTTON_T3_LIST[0][0], BUTTON_T3_LIST[0][1])
                        mouse.click(SPE_SUMMON_BATTLE_STAT[0][0], SPE_SUMMON_BATTLE_STAT[0][1])
                        mouse.click(SPE_SUMMON_BATTLE_CONFIRM[0], SPE_SUMMON_BATTLE_CONFIRM[1])
                        self.magic_grant = True
                        del duel.hand_card[index]
                        del self.card_list[index]
                        duel.hand_card_num -= 1
                        cancle()
                        tick()
                        break
                    elif '力量' in self.card_list[index] and self.magic_grant:
                        print('发动力量')
                        duel.reflesh()
                        point = duel.hand_card_pos[index]
                        mouse.slide(point[0], point[1], 'up')
                        mouse.click(BUTTON1[0], BUTTON1[1])
                        tick()
                        mouse.click(EFFECT_SELECT[1][0], EFFECT_SELECT[1][1])
                        mouse.click(EFFECT_CONFIRM[0], EFFECT_CONFIRM[1])
                        tick()
                        mouse.click(EFFECT_SELECT[0][0], EFFECT_SELECT[0][1])
                        mouse.click(EFFECT_CONFIRM[0], EFFECT_CONFIRM[1])
                        cancle()
                        tick()
                        self.power = True
                        duel.hand_card_num -= 1
                        del duel.hand_card[index]
                        del self.card_list[index]
                        break
                    elif '继承之力' in self.card_list[index] and self.power:
                        print('发动继承之力')
                        duel.reflesh()
                        point = duel.hand_card_pos[index]
                        mouse.slide(point[0], point[1], 'up')
                        mouse.click(BUTTON1[0], BUTTON1[1])
                        tick()
                        mouse.click(EFFECT_SELECT[1][0], EFFECT_SELECT[1][1])
                        mouse.click(EFFECT_CONFIRM[0], EFFECT_CONFIRM[1])
                        tick()
                        mouse.click(EFFECT_SELECT[0][0], EFFECT_SELECT[0][1])
                        mouse.click(EFFECT_CONFIRM[0], EFFECT_CONFIRM[1])
                        cancle()
                        tick()
                        self.attack = True
                        duel.hand_card_num -= 1
                        del duel.hand_card[index]
                        del self.card_list[index]
                        break
                if self.attack:
                    break 

    def battle_phase(self):
        if self.attack:
            print('开始战斗')
            duel.attack(1, 1)
            cancle(2)
            tick(2)
            analyze.routine_check('end')
    
    def duel_end_act(self):
        super(Mai, self).duel_end_act()
        self.card_list = []
        self.hand_check = True
        self.add_card = 1
        self.magic_monster = False
        self.magic_grant = False
        self.power = False
        self.final_turn = False
        self.attack = False
        self.ready_card = False
        self.deck_num = 20
        self.ready_num = 0


mai_routine = Mai()
        
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
    # default.run()
    mai_routine.run()

if __name__ == '__main__':
    main()
    # analyze.online_ocr.check_connect()
    # get_color()
    # print(analyze.check_deck_status())
    # print(analyze.hand_card(HAND_CARD_3))
    # analyze.routine_check()
    # print(duel.phase)
    # print(analyze.check_handcard_num())
