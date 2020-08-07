"""
    ftp文件服务器
"""
from socket import *
from threading import Thread
import sys, time
from EruptSimultaneously.day4.ftpTransfer import *

HOST = '0.0.0.0'
POST = 8888
SERVER_ADDR = (HOST, POST)
sockfd = socket()
sockfd.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
sockfd.bind(SERVER_ADDR)
sockfd.listen(10)

print("Listen to the port 8888......")
while True:
    try:
        connfd, addr = sockfd.accept()
        ftp = FTPServer(connfd)
    except KeyboardInterrupt:
        sys.exit("服务器退出")
    except Exception as e:
        print(e)
        continue
    t = Thread(target=ftp.handle)
    t.start()


