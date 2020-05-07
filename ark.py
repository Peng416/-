import os
import sys
import pyautogui as auto
import time
import keyboard
import configparser
from PIL import Image


'''属性设置'''
config = configparser.ConfigParser()
config.read('config.ini', encoding='utf-8')
Apath = config.get('main', 'Apath')  # 模拟器图片位置
pausetime = int(config.get('main', 'pausetime'))  # 点击间隔
ip = config.get('main', 'ip')  # 模拟器端口ip地址
c = config.get('main', 'c')  # 图片识别率
Is = config.get('main', 'Is')  # 默认分辨率为1280*720

'''定义变量'''


'''函数部分'''
# 从模拟器上截图并返回图片


def screenshot():
    os.system(f"adb shell screencap -p {Apath}/screenshot.png")
    os.system("adb pull /sdcard/screenshot.png")


# 得到当前分辨率
def getT_is():
    filename = 'screenshot.png'
    try:
        os.remove(filename)
    except:
        pass
    screenshot()
    try:
        global hx
        global hy
        global True_image_size
        img = Image.open(filename)
        True_image_size = img.size
        maxSize = max(True_image_size)
        minSize = min(True_image_size)
        hx = maxSize//2
        hy = minSize//2
        return hx, hy, True_image_size
    except:
        print('abd连接失败，请打开模拟器后重试')
        sys.exit(0)


# 触摸输入
def tap(x, y):  # 点击坐标 x，y
    print(f'点击坐标 {x} {y}')
    os.system(f'adb shell input tap {x} {y}')

# 触摸选中的图片


def touch(img_name, pausetime):
    screenshot()
    p = auto.locate(f'./picture/{Is}/{img_name}',
                    'screenshot.png', confidence=c)
    if p != None:
        x, y = auto.center(p)
        tap(x, y)
        time.sleep(pausetime)
    elif p == None:
        print('图片未识别')

# 对图片进行多次选择分析


def touchlist(imglist, pausetime, stage):
    while True:
        screenshot()
        for img_name in imglist:
            p = auto.locate(f'./picture/{Is}/{img_name}', 'screenshot.png', confidence=c)
            if stage == 'start':  # 开始阶段
                if p != None:  # 点击op按钮
                    x, y = auto.center(p)
                    tap(x, y)
                    time.sleep(pausetime)
                    return None
                elif p != None:  # 退出理智不足的画面
                    print('\n----理智不足----')
                    sys.exit(0)
            elif stage == 'end':  # 结束阶段
                if p != None:  # 点击结算画面
                    x, y = auto.center(p)
                    tap(x, y)
                    time.sleep(pausetime)
                    return None
                elif p != None:  # 任务失败 多点一次
                    tap(hx, hy)
                    time.sleep(pausetime)
                    return None


def compare(img_name):
    screenshot()
    p = auto.locate(f'./picture/{Is}/{img_name}',
                    'screenshot.png', confidence=c)
    if p != None:
        return True
    else:
        return False


def battle(times):
    i = 0
    n = int(times)
    while i < n:
        i += 1
        print(f'--------第{i}次战斗开始--------')
        touch('start_battle.png', pausetime)
        touchlist(('os.png', 'lzbz.png'), pausetime, 'start')
        while True:
            if compare("confidence.png") == False:
                time.sleep(6)
                print('战斗进行中...')
            else:
                break
        touchlist(("confidence.png",'defeat.png'), pausetime,'end')
        print(f"---------第{i}次战斗结束--------")
        while compare("start_battle.png") == False:
            time.sleep(3)


'''初始化部分'''
print("欢迎使用明日方舟自定义挂机程序\n-------------------按下Enter键开始-------------------\n")
os.system('pause')
print("\n--------初始化中--------\n")
os.system(f'adb connect {ip}')
getT_is()
print(f'配置图片分辨率:{Is}\n当前实际分辨率:{True_image_size} 中心值:({hx},{hy})\n点击间隔:{pausetime}\n图片识别率:{c}')
print('\n--------初始化成功--------\n请选择模式 F1无限模式 F2自定义次数')


'''主代码部分'''
key = keyboard.read_key(suppress=False)
if key == "f1":
    os.system('pause')
    battle(99999)
elif key == "f2":
    os.system('pause')
    times = input("请输入次数")
    battle(times)