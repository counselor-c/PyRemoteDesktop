import tkinter
import tkinter.messagebox
import struct
import socket
import numpy as np
from PIL import Image, ImageTk
import threading
from cv2 import cv2
import time
import client_file
from tkinter import filedialog
import json

root = tkinter.Tk()

# 画面周期
IDLE = 0.05

# 屏幕显示画布
showcan = None

# socket缓冲区大小
bufsize = 1024

# 线程
th = None

# 全局文件
file_Up = None
file_Down = None

# 全局控件
lbx = None

# 选择连接
port_select = 9996
soc_select = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 初始化远程操作socket
port_remote = 9999
soc_remote = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 初始化上传链接
port_up = 9998
soc_up = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 初始化下载链接
port_down = 9997
soc_down = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


def ShowScreen():
    # 判断是否填入了主机地址
    if not entry.get():
        tkinter.messagebox.showinfo("提示", "请输入目标主机IP地址")
        return
    global showcan, root, wscale
    showcan = tkinter.Toplevel(root)
    threading.Thread(target=run).start()
    print("wtf")


def Up():
    global soc_up, port_up, port_select, soc_select, file_Up
    filepath = file_Up  # 上传文件路径
    host = entry.get().strip("\n")
    if filepath:

        soc_select.connect((host, port_select))
        flag = struct.pack('>I', 2)
        soc_select.send(flag)
        soc_select.close()

        soc_up.connect((host, port_up))
        client_file.client_file_up(file_path=filepath, soc_up=soc_up)
    else:
        tkinter.messagebox.showinfo("提示", "请输入所上传文件路径")
        return


def Down():
    global soc_down, port_down, port_select, soc_select, lbx

    filename = lbx.selection_get()
    if filename:

        client_file.client_file_down(filename=filename, soc_down=soc_down)
        soc_down.close()
    else:
        tkinter.messagebox.showinfo("提示", "请输入下载文件名")
        return


def UpfilesW():
    if not entry.get():
        tkinter.messagebox.showinfo("提示", "请输入目标主机IP地址")
        return
    global file_Up
    top1 = tkinter.Toplevel(root)
    ack_btn = tkinter.Button(top1, text="上传", command=Up)
    ack_btn.grid(row=2, column=1, padx=0, pady=10, ipadx=30, ipady=0)
    file_Up = filedialog.askopenfilename()


def DownfilesW():
    global soc_down, port_down, port_select, soc_select, lbx
    if not entry.get():
        tkinter.messagebox.showinfo("提示", "请输入目标主机IP地址")
        return
    host = entry.get().strip("\n")
    soc_select.connect((host, port_select))
    flag = struct.pack('>I', 3)
    soc_select.send(flag)
    soc_select.close()

    soc_down.connect((host, port_down))
    listb = soc_down.recv(1024).decode("utf-8")
    filelist = json.loads(listb)  # filelist为服务器指定目录下的文件

    top2 = tkinter.Toplevel(root)
    lbx = tkinter.Listbox(top2)
    for file in filelist:
        lbx.insert("end", str(file))
    lbx.grid(row=1)

    ack_btn = tkinter.Button(top2, text="下载", command=Down)
    ack_btn.grid(row=2, column=1, padx=0, pady=10, ipadx=30, ipady=0)


# 主窗口布局
entry = tkinter.Entry(root)
entry.grid(row=1)
entry.insert(0, "192.168.216.135")  # 设置默认连接
show_btn = tkinter.Button(root, text="Show", command=ShowScreen)
show_btn.grid(row=2, column=1, padx=0, pady=10, ipadx=30, ipady=0)
up_btn = tkinter.Button(root, text="Upload", command=UpfilesW)
up_btn.grid(row=5, column=1, padx=0, pady=10, ipadx=30, ipady=0)
down_btn = tkinter.Button(root, text="Download", command=DownfilesW)
down_btn.grid(row=7, column=1, padx=0, pady=10, ipadx=30, ipady=0)

last_send = time.time()


def BindEvents(canvas):
    global soc_remote
    '''
    处理事件
    '''

    def EventDo(data):
        soc_remote.sendall(data)

    # 鼠标左键

    def LeftDown(e):
        return EventDo(struct.pack('>BBHH', 1, 100, int(e.x), int(e.y)))

    def LeftUp(e):
        return EventDo(struct.pack('>BBHH', 1, 117, int(e.x), int(e.y)))

    canvas.bind(sequence="<1>", func=LeftDown)
    canvas.bind(sequence="<ButtonRelease-1>", func=LeftUp)

    # 鼠标右键
    def RightDown(e):
        return EventDo(struct.pack('>BBHH', 3, 100, int(e.x), int(e.y)))

    def RightUp(e):
        return EventDo(struct.pack('>BBHH', 3, 117, int(e.x), int(e.y)))

    canvas.bind(sequence="<3>", func=RightDown)
    canvas.bind(sequence="<ButtonRelease-3>", func=RightUp)

    # 鼠标滚轮
    def Wheel(e):
        if e.delta < 0:
            return EventDo(struct.pack('>BBHH', 2, 0, int(e.x), int(e.y)))
        else:
            return EventDo(struct.pack('>BBHH', 2, 1, int(e.x), int(e.y)))

    canvas.bind(sequence="<MouseWheel>", func=Wheel)

    def WheelDown(e):
        return EventDo(struct.pack('>BBHH', 2, 0, int(e.x), int(e.y)))

    def WheelUp(e):
        return EventDo(struct.pack('>BBHH', 2, 1, int(e.x), int(e.y)))

    canvas.bind(sequence="<Button-4>", func=WheelUp)
    canvas.bind(sequence="<Button-5>", func=WheelDown)

    # 鼠标滑动
    # 100ms发送一次
    def Move(e):
        global last_send
        cu = time.time()
        if cu - last_send > IDLE:
            last_send = cu
            sx, sy = int(e.x), int(e.y)
            return EventDo(struct.pack('>BBHH', 4, 0, sx, sy))

    canvas.bind(sequence="<Motion>", func=Move)

    # 键盘
    def KeyDown(e):
        return EventDo(struct.pack('>BBHH', e.keycode, 100, int(e.x), int(e.y)))

    def KeyUp(e):
        return EventDo(struct.pack('>BBHH', e.keycode, 117, int(e.x), int(e.y)))

    canvas.bind(sequence="<KeyPress>", func=KeyDown)
    canvas.bind(sequence="<KeyRelease>", func=KeyUp)


def run():
    global soc_remote, showcan, soc_select, port_select, port_remote

    host = entry.get().strip("\n")

    soc_select.connect((host, port_select))
    flag = struct.pack('>I', int(1))
    soc_select.send(flag)
    soc_select.close()

    soc_remote.connect((host, port_remote))

    print(soc_remote)
    len_byte = soc_remote.recv(4)

    le = struct.unpack(">I", len_byte)[0]
    imb = b''

    # 一次最大传输buffsize数据，
    # 首次获取原始界面
    while le > bufsize:
        t = soc_remote.recv(bufsize)
        imb += t
        le -= len(t)
    while le > 0:
        t = soc_remote.recv(le)
        imb += t
        le -= len(t)
    data = np.frombuffer(imb, dtype=np.uint8)
    img = cv2.imdecode(data, cv2.IMREAD_COLOR)
    # imt = cv2.resize(img, (1920, 1080))  # 对图片进行放缩
    imsh = cv2.cvtColor(img, cv2.COLOR_RGB2RGBA)
    imi = Image.fromarray(imsh)
    imgTK = ImageTk.PhotoImage(image=imi)

    cv = tkinter.Canvas(showcan, width=1578, height=888, bg="white")
    cv.focus_set()
    BindEvents(cv)
    cv.pack()
    cv.create_image(0, 0, anchor=tkinter.NW, image=imgTK)

    # 差异化传输
    while True:
        len_byte = soc_remote.recv(4)
        le = struct.unpack(">I", len_byte)[0]
        imb = b''
        while le > bufsize:
            t = soc_remote.recv(bufsize)
            imb += t
            le -= len(t)
        while le > 0:
            t = soc_remote.recv(le)
            imb += t
            le -= len(t)
        data = np.frombuffer(imb, dtype=np.uint8)
        ims = cv2.imdecode(data, cv2.IMREAD_COLOR)
        img = img + ims
        imt = cv2.resize(img, (1578, 888))  # 对图片进行放缩
        imsh = cv2.cvtColor(imt, cv2.COLOR_RGB2RGBA)
        imi = Image.fromarray(imsh)
        imgTK.paste(imi)


root.mainloop()
