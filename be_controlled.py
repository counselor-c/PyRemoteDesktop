import pyautogui
import numpy as np
import cv2
from PIL import ImageGrab
import socket
import struct
import threading
import mouse
import keyboard
from keyboard_cast import keycodeMappingWin
import server_file

keyMapping = keycodeMappingWin

host = "0.0.0.0"

# 选择功能连接
port_select = 9996
soc_select = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
soc_select.bind((host, port_select))
soc_select.listen(1)

# 远程操作链接
buffsize = 1024
port_remote = 9999
soc_remote = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
soc_remote.bind((host, port_remote))
soc_remote.listen(1)
img = None

# 文件上传链接
port_up = 9998
soc_up = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
soc_up.bind((host, port_up))
soc_up.listen(1)

# 文件下载链接
port_down = 9997
soc_down = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
soc_down.bind((host, port_down))
soc_down.listen(1)

# 滚轮灵敏度
SCROLL_NUM = 5


def ctrl(conn):
    '''
    读取控制命令，并在本机还原操作
    '''
    global keyMapping

    # key 控件参数
    # op操作参数
    def Op(key, op, ox, oy):
        # print(key, op, ox, oy)
        if key == 4:
            # 鼠标移动
            mouse.move(ox, oy)
        elif key == 1:
            if op == 100:
                # 左键按下
                pyautogui.mouseDown(button=pyautogui.LEFT)
            elif op == 117:
                # 左键弹起
                pyautogui.mouseUp(button=pyautogui.LEFT)
        elif key == 2:
            # 滚轮事件
            if op == 0:
                # 向上
                pyautogui.scroll(-SCROLL_NUM)
            else:
                # 向下
                pyautogui.scroll(SCROLL_NUM)
        elif key == 3:
            # 鼠标右键
            if op == 100:
                # 右键按下
                pyautogui.mouseDown(button=pyautogui.RIGHT)
            elif op == 117:
                # 右键弹起
                pyautogui.mouseUp(button=pyautogui.RIGHT)
        else:
            k = keyMapping.get(key)
            if k is not None:
                if op == 100:
                    pyautogui.keyDown(k)
                elif op == 117:
                    pyautogui.keyUp(k)

    base_len = 6
    while True:
        cmd = b''
        rest = base_len - 0
        while rest > 0:
            cmd += conn.recv(rest)
            rest -= len(cmd)
        key = cmd[0]
        op = cmd[1]
        x = struct.unpack('>H', cmd[2:4])[0]
        y = struct.unpack('>H', cmd[4:6])[0]
        Op(key, op, x, y)


def handle(conn):
    # 初始图片传输阶段
    global img
    img = np.asarray(ImageGrab.grab())
    _, imb = cv2.imencode(".png", img)
    lenb = struct.pack(">I", len(imb))
    conn.send(lenb)
    conn.send(imb)

    # 后续差异化传输阶段
    while True:
        cv2.waitKey(100)
        image = np.asarray(ImageGrab.grab())
        sub = image - img
        if (sub == 0).all():
            continue
        img = image
        _, imb = cv2.imencode(".png", sub)
        lent = struct.pack(">I", len(imb))
        conn.send(lent)
        conn.send(imb)


while True:
    conn0, add0 = soc_select.accept()
    fb = conn0.recv(4)
    flag = struct.unpack('>I', fb)[0]
    print(flag)
    if flag == 1:
        conn1, add1 = soc_remote.accept()
        print(flag)
        threading.Thread(target=handle, args=(conn1,)).start()
        threading.Thread(target=ctrl, args=(conn1,)).start()

    if flag == 2:
        conn2, add2 = soc_up.accept()
        threading.Thread(target=server_file.up_file, args=(conn2,)).start()

    if flag == 3:
        conn3, add3 = soc_down.accept()
        threading.Thread(target=server_file.down_file, args=(conn3,)).start()
