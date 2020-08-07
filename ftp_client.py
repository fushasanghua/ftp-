from socket import *
import os
from EruptSimultaneously.day4.ftpTransfer import *

def request(sockfd):
    while True:
        print("\n××××××××××命令选项×××××××××××")
        print("************list************")
        print("**********get file**********")
        print("**********put file**********")
        print("************quit************")
        print("××××××××××××××××××××××××××××")
        cmd = input(">>")
        ftp = FTPClient(sockfd)
        if cmd == "list":
            ftp.do_list()
        elif cmd == "quit":
            ftp.quit()
        elif cmd[:3] == "get":
            filename = cmd.split(' ')[-1]
            ftp.download(filename)
        elif cmd[:3] == "put":
            filename = cmd.split(' ')[-1]
            ftp.upload(filename)
        else:
            print("Error cmd!")

HOST = '0.0.0.0'
POST = 8888
SERVER_ADDR = (HOST, POST)
sockfd = socket()
try:
    sockfd.connect(SERVER_ADDR)
except Exception as e:
    print("连接服务器失败")
    os._exit(0)
else:
    print("""
        picture     txt
    """)
    cls = input("请输入文件类型：")
    if cls not in ["picture","txt"]:
        print("Error Type!")
        os._exit(0)
    else:
        sockfd.send(cls.encode())
        request(sockfd)
sockfd.close()
