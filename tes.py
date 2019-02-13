import os
import paramiko

print(os.name)

if os.name == "nt" or (os.name == "java" or os._name=="nt"):
    print("windows")

seq = [1,2,3,4,5,6,7,8]
print([seq[i:i+2] for i in range(0, len(seq), 2)])

# 定义一个类，表示一台远端linux主机
class Linux(object):
    def __init__(self, ip, username, password, timeout=30):
        self.ip = ip
        self.username = username
        self.password = password
        self.timeout = timeout
        # transport和chanel
        self.t = ''
        self.chan = ''
        # 链接失败的重试次数
        self.try_times = 3

    # 调用该方法连接远程主机
    def connect(self):
         pass

    # 断开连接
    def close(self):
        pass

    # 发送要执行的命令
    def send(self, cmd):
        pass

    # get单个文件
    def sftp_get(self, remotefile, localfile):
        t = paramiko.Transport(sock=(self.ip, 22))
        t.connect(username=self.username, password=self.password)
        sftp = paramiko.SFTPClient.from_transport(t)
        sftp.get(remotefile, localfile)
        t.close()

    # put单个文件
    def sftp_put(self, localfile, remotefile):
        t = paramiko.Transport(sock=(self.ip, 22))
        t.connect(username=self.username, password=self.password)
        sftp = paramiko.SFTPClient.from_transport(t)
        sftp.put(localfile, remotefile)
        t.close()

if __name__ == '__main__':
    remotefile = r'/home/sea/test/xxoo.txt'
    localfile = r'E:\PythonFiles\Learn\ooxx.txt'
    host = Linux('192.168.180.128', 'root', '1234')

    host.sftp_get(remotefile, localfile)
