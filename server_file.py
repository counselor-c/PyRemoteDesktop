import os
import socket
import threading
import struct
import json


def up_file(conn):
    while 1:
        file_info_size = struct.calcsize('128sl')
        # 接收文件名与文件大小信息
        buf = conn.recv(file_info_size)
        # 判断是否接收到文件头信息
        if buf:
            # 获取文件名和文件大小
            filename, file_size = struct.unpack('128sl', buf)
            fn = filename.strip(b'\00')
            fn = fn.decode()
            print('file new name is {0}, filesize is {1}'.format(str(fn), file_size))

            recvd_size = 0  # 定义已接收文件的大小
            # 存储在该脚本所在目录下面
            with open('./' + str(fn), 'wb') as fp:
                print('start receiving...')

                # 将分批次传输的二进制流依次写入到文件
                while not recvd_size == file_size:
                    if file_size - recvd_size > 1024:
                        data = conn.recv(1024)
                        recvd_size += len(data)
                    else:
                        data = conn.recv(file_size - recvd_size)
                        recvd_size = file_size
                    fp.write(data)
                print('end receive...')

        # 传输结束断开连接
        break


def down_file(conn):
    path = "./test_pic/"
    # 先返回自身目录下的文件列表
    filelist = os.listdir(path=path)
    listb = json.dumps(filelist)
    conn.send(listb.encode("utf-8"))

    byte = conn.recv(struct.calcsize('128s'))
    fp = byte.strip(b'\00')  # 重要，不知道为什么会有空格，是否是pack自己加了空格
    filename = fp.decode('utf-8')
    file_path = path + filename
    print(file_path)

    with open(file_path, 'rb') as fp:
        file_size = os.stat(file_path).st_size
        fhead = struct.pack('l', file_size)
        conn.send(fhead)

        while True:
            data = fp.read(1024)
            if not data:
                print('{0} file send over...'.format(filename))
                break
            conn.send(data)
