"""
    文件传输类
"""
from socket import *
import os, time, sys

ftp_path = "/home/ariana/Python/2Second/EruptSimultaneously/day4/FTP/"

class FTPServer:
    def __init__(self, connfd):
        self.connfd = connfd
        self.FTP_PATH = ftp_path

    def handle(self):
        print("Connect from", self.connfd.getpeername())
        cls = self.connfd.recv(1024).decode()
        self.FTP_PATH = ftp_path + cls + '/'
        while True:
            data = self.connfd.recv(1024).decode()
            if not data or data[0] == 'Q':
                return
            elif data[0] == 'L':
                self.do_list()
            elif data[0] == 'D':
                filename = data[1:]
                self.do_get(filename)
            elif data[0] == 'U':
                filename = data[1:]
                self.do_put(filename)

    def do_list(self):
        #获取路径下的文件列表
        files = os.listdir(self.FTP_PATH)
        if not files:
            self.connfd.send("empty!".encode())
        else:
            self.connfd.send(b'OK')
        fs = ''
        for file in files:
            #保证不是隐藏文件并且他是普通文件
            if file[0] != '.' and os.path.isfile(self.FTP_PATH + file):
                fs += file + '\n'   #人为加一个边界，避免不断地send出现粘包
        self.connfd.send(fs.encode())

    def do_get(self, filename):
        try:
            fd = open(self.FTP_PATH + filename, "rb")
        except Exception:
            self.connfd.send("文件不存在".encode())
            return
        else:
            self.connfd.send(b'OK')
            time.sleep(0.1)
        while True:
            data = fd.read(1024)
            if not data:
                time.sleep(0.1)
                self.connfd.send(b'##')
                break
            self.connfd.send(data)

    def do_put(self, filename):
        if os.path.exists(self.FTP_PATH + filename):
            self.connfd.send("该文件已存在".encode())
            return
        else:
            self.connfd.send(b'OK')
        fd = open(self.FTP_PATH + filename, "wb")
        while True:
            data = self.connfd.recv(1024)
            if data == b'##':
                break
            fd.write(data)
        fd.close()


class FTPClient:
    def __init__(self, sockfd):
        self.sockfd = sockfd

    def do_list(self):
        self.sockfd.send(b'L')  #协议：L发送请求
        #等待回复
        data = self.sockfd.recv(128).decode()
        if "OK" == data:
            data = self.sockfd.recv(1024)
            print(data.decode())
        else:
            print(data)

    def quit(self):
        self.sockfd.send(b'Q')
        self.sockfd.close()
        sys.exit("谢谢使用")

    def download(self, filename):
        self.sockfd.send(('D' + filename).encode())
        data = self.sockfd.recv(128).decode()
        if data == "OK":
            fd = open(filename, "wb")
            while True:
                data = self.sockfd.recv(1024)
                if data == b'##':
                    break
                fd.write(data)
            fd.close()
        else:
            print(data)


    def upload(self, filename):
        try:
            fd = open(filename, "rb")
        except Exception:
            print("没有该文件！")
            return

        self.sockfd.send(('U' + filename).encode())
        data = self.sockfd.recv(128).decode()
        if data == 'OK':
            while True:
                data = fd.read(1024)
                if not data:
                    time.sleep(0.1)
                    self.sockfd.send(b'##')
                    break
                self.sockfd.send(data)
            fd.close()
        else:
            print(data)