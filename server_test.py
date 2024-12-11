import tkinter
import pyautogui
import os

root = tkinter.C

top = tkinter.Toplevel(root)
cv = tkinter.Canvas(top)

filelist = os.listdir(path="./test_pic")
print(filelist)


def BindEvents(canvas):
    '''
    处理事件
    '''

    # def EventDo(data):
    #     soc.sendall(data)

    # 鼠标左键

    def LeftDown(e):
        print("left mouse down")
        # print(e)

    def LeftUp(e):
        print("left mouse up")
        # print(e)

    canvas.bind(sequence="<1>", func=LeftDown)
    canvas.bind(sequence="<ButtonRelease-1>", func=LeftUp)

    # 鼠标右键
    def RightDown(e):
        # print(e)
        print("right mouse down")

    def RightUp(e):
        # print(e)
        print("right mouse up")

    canvas.bind(sequence="<3>", func=RightDown)
    canvas.bind(sequence="<ButtonRelease-3>", func=RightUp)

    # 鼠标滚轮

    def Wheel(e):
        if e.delta < 0:
            # print(e)
            print("wheel up")

        # else:

    # print(e)

    canvas.bind(sequence="<MouseWheel>", func=Wheel)

    def WheelDown(e):
        # print(e)
        print("wheel up")

    def WheelUp(e):
        # print(e)
        print("wheel down")

    canvas.bind(sequence="<Button-4>", func=WheelUp)
    canvas.bind(sequence="<Button-5>", func=WheelDown)

    # 鼠标滑动
    # 100ms发送一次
    def Move(e):
        # print(e)
        print("mouse move")

    canvas.bind(sequence="<Motion>", func=Move)

    # 键盘
    def KeyDown(e):
        # print(e)
        print("Key down")

    def KeyUp(e):
        # print(e)
        print("key up")

    canvas.bind(sequence="<KeyPress>", func=KeyDown)
    canvas.bind(sequence="<KeyRelease>", func=KeyUp)


cv.focus_set()
cv.grid()
BindEvents(canvas=cv)

root.mainloop()

# def ShowScreen():
#     cv = tkinter.Canvas(root, width=1568, height=864, bg="white")
#     cv.focus_set()
#     cv.grid()
#     cv.create_rectangle(10, 10, 110, 110)
#
#
# show_btn = tkinter.Button(root, text="Show", command=ShowScreen)
# show_btn.grid(row=2, column=1, padx=0, pady=10, ipadx=30, ipady=0)
#
# root.mainloop()
# 画布无法实现。。。
# h, w, _ = img.shape
# fixh, fixw = h, w  # 接受的图片数据初始大小，方便后续放缩
# imsh = cv2.cvtColor(img, cv2.COLOR_RGB2RGBA)
# imi = Image.fromarray(imsh)
# imgTK = ImageTk.PhotoImage(image=imi)
# cv = tkinter.Canvas(showcan, width=w, height=h, bg="white")
# cv.focus_set()
# cv.pack()
# cv.create_image(0, 0, anchor=tkinter.NW, image=imgTK)
# h = int(h * scale)
# w = int(w * scale)
#
# while True:
#     if wscale:
#         h = int(fixh * scale)
#         w = int(fixw * scale)
#         cv.config(width=w, height=h)
#         wscale = False
#
#     len_byte = soc.recv(4)
#     le = struct.unpack(">I", len_byte)[0]
#     imb = b''
#     while le > buffsize:
#         t = soc.recv(buffsize)
#         imb += t
#         le -= len(t)
#     while le > 0:
#         t = soc.recv(le)
#         imb += t
#         le -= len(t)
#
#     data = np.frombuffer(imb, dtype=np.uint8)
#     ims = cv2.imdecode(data, cv2.IMREAD_COLOR)
#
#     img = img + ims
#
#     imt = cv2.resize(img, (w, h))  # 对图片进行放缩
#     imsh = cv2.cvtColor(imt, cv2.COLOR_RGB2RGBA)
#     imi = Image.fromarray(imsh)
#     imgTK.paste(imi)
#
