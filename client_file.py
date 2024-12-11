import socket
import os
import sys
import struct


# 此处自行定义一个文件传输协议，先以2B字节传递文件名，后以1B字节传递文件长度

# host = "localhost"
# upload_port = 9998
# download_port = 9997
#
# soc_up = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# soc_up.connect((host, upload_port))
#
# soc_down = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# soc_down.connect((host, download_port))


def client_file_up(file_path, soc_up):
    filename = os.path.basename(file_path)
    file_size = os.stat(file_path).st_size

    fhead = struct.pack('128sl', filename.encode('utf-8'), file_size)
    soc_up.send(fhead)

    fp = open(file_path, 'rb')
    while True:
        data = fp.read(1024)
        if not data:
            print('{0} file send over...'.format(filename))
            break
        soc_up.send(data)

    soc_up.close()


def e_client_fildown(filename, soc_down):
    fhead = struct.pack("128s", filename.encode('utf-8'))
    # 发送要请求的文件名
    soc_down.send(fhead)

    buf = soc_down.recv(struct.calcsize('128s'))

    if buf:
        # 获取文件大小
        file_size = struct.unpack('l', buf)[0]  # 有点莫名其妙。。为什么会是tuple类型?

        recvd_size = 0  # 定义已接收文件的大小
        # 存储在该脚本所在目录下面
        with open('./' + filename, 'wb') as fp:
            print('start receiving...')

            # 将分批次传输的二进制流依次写入到文件
            while not recvd_size == file_size:
                if file_size - recvd_size > 1024:
                    data = soc_down.recv(1024)
                    recvd_size += len(data)
                else:
                    data = soc_down.recv(file_size - recvd_size)
                    recvd_size = file_size
                fp.write(data)
            print('end receive...')

    soc_down.close()

# client_file_up("./test_pic/1.png")
# client_file_down("1.png")
