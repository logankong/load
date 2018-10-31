# -*- coding:utf-8 -*-
import multiprocessing
import Pysensor
import time
import select
import CRedis
import os
import signal
import sys
import ip
import Report
import random


class Tianxun(object):
    """天巡性能测试"""

    def __init__(self):
        self.is_running = True
        self.num = CLIENT_MAC_NUM / HOTSPORT_MAC_NUM
        self.fd_args = {}
        self.fds = []

    def sig_handler(self, signo, frame):
        self.is_running = False
        self.r.set('is_report', 0)

    def getMsg(self, fd):
        inputs = [fd]
        # get_log = open('logs/get.log', 'a+')
        while True:
            try:
                readable, writable, exceptional = select.select(inputs, [], [], 10)
            except select.error:
                for s in readable:
                    if s is fd:
                        Pysensor.CloseSensor(fd)
                break
            for s in readable:
                if s is fd:
                    ctime_GetMsg = time.time()
                    res_GetMsg = Pysensor.GetMsg(fd)
                    self.record_get(res_GetMsg, ctime_GetMsg, time.time())
        else:
            Pysensor.CloseSensor(fd)
        # get_log.close()

    def sendMsg(self, fd):
        hotsport_num_list = list(range(HOTSPORT_MAC_NUM))
        client_num_list = list(range(CLIENT_MAC_NUM))
        temp_hotsport_num = []
        temp_client_num = []
        while self.is_running:
            hotsport_mac_list = ip.macSelfAdd(HOTSPORT_MAC, CLIENT_MAC_NUM, fd)
            client_mac_list = ip.macSelfAdd(hotsport_mac_list[CLIENT_MAC_NUM - 1], CLIENT_MAC_NUM, fd)

            # 生成wifi列表
            dif_hotsport = list(set(hotsport_num_list).difference(set(temp_hotsport_num)))
            hotsport_loop = random.sample(dif_hotsport, int(HOTSPORT_MAC_NUM * HOTSPORT_MAC_NUM_PERCENT / 100))
            temp_hotsport_num.extend(hotsport_loop)
            if len(temp_hotsport_num) == len(hotsport_num_list):
                temp_hotsport_num = []

            # 生成户端列表
            dif_client = list(set(client_num_list).difference(set(temp_client_num)))
            client_loop = random.sample(dif_client, int(CLIENT_MAC_NUM * CLIENT_MAC_NUM_PERCENT / 100))
            temp_client_num.extend(client_loop)
            if len(temp_client_num) == len(client_num_list):
                temp_client_num = []

            tname_sendMsg = 'sendMsg'
            ctime_sendMsg = time.time()

            tname_SendHotspotInfo = 'SendHotspotInfo'  # 创建热点
            ctime_SendHotspotInfo = time.time()
            for i in hotsport_loop:
                hotsportName = HOTSPORTNAME + str(fd) + '_' + str(i)
                res_SendHotspotInfo = Pysensor.SendHotspotInfo(fd, hotsport_mac_list[i], hotsportName, 1, 6, 0, 0, 0)
                res = self.record(tname_SendHotspotInfo, res_SendHotspotInfo, ctime_SendHotspotInfo, time.time(), fd)
                if res:
                    fd = res

            tname_SendStationInfo = 'SendStationInfo'  # 终端信息
            ctime_SendStationInfo = time.time()
            for i in client_loop:
                res_SendStationInfo = Pysensor.SendStationInfo(
                    fd, client_mac_list[i], ip.randomMAC(), "KLG-Test1\aKLG-Test2")
                res = self.record(tname_SendStationInfo, res_SendStationInfo, ctime_SendStationInfo, time.time(), fd)
                if res:
                    fd = res

            tname_SendHotspot2Station = 'SendHotspot2Station'  # 终端-热点连接
            ctime_SendHotspot2Station = time.time()
            for i in hotsport_loop:  # wifi数量
                client_str = ''
                for x in range(i * self.num, self.num + i * self.num):
                    client_str += client_mac_list[x] + ";"
                res_SendHotspot2Station = Pysensor.SendHotspot2Station(fd, hotsport_mac_list[i], client_str)
                res = self.record(tname_SendHotspot2Station, res_SendHotspot2Station, ctime_SendHotspot2Station, time.time(), fd)
                if res:
                    fd = res

            res = self.record(tname_sendMsg, 'succeed', ctime_sendMsg, time.time(), fd)
            if res:
                    fd = res
            time.sleep(4)
        else:
            Pysensor.CloseSensor(fd)

    def record(self, tname, res, ctime, etime, fd=0):
        rtime = etime - ctime
        if res == 'succeed':
            self.r.lpush(tname, rtime)
            self.r.incr(tname + '_success')

            return False
        else:
            self.r.incr(tname + '_fail')
            if fd == 0:
                return False
            arg = self.fd_args[fd]
            connect_log = open('logs/connect.log', 'a+')
            strtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

            log_str = 'err\t' + str(fd) + '\t' + str(arg) + '\t' + strtime + '\t' + str(res) + '\t' + tname + '\n'
            connect_log.write(log_str)

            res_GetMsg_error = Pysensor.CloseSensor(fd)
            log_str = 'cls\t' + str(fd) + '\t' + str(arg) + '\t' + strtime + '\t' + str(res_GetMsg_error) + '\n'
            connect_log.write(log_str)
            connect_log.close()

            time.sleep(60)
            connect_log = open('logs/connect.log', 'a+')
            strtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            res_Connect2txByIpaddr = Pysensor.Connect2txByIpaddr(*arg)
            log_str = 'new\t' + str(res_Connect2txByIpaddr) + '\t' + str(arg) + strtime + '\n'
            connect_log.write(log_str)

            self.fd_args[res_Connect2txByIpaddr[0]] = arg
            del self.fd_args[fd]

            self.fds.append(res_Connect2txByIpaddr[0])
            self.fds.remove(fd)
            connect_log.close()

            return res_Connect2txByIpaddr[0]

    def record_get(self, res, ctime, etime):
        rtime = etime - ctime
        self.r.lpush('getMsg_' + res, rtime)
        self.r.incr('getMsg_' + res + '_success')

    def main(self, method, args):
        signal.signal(signal.SIGINT, self.sig_handler)
        signal.signal(signal.SIGTERM, self.sig_handler)

        self.r = CRedis.CRedis()
        self.r.clear()
        path = os.path.dirname(os.path.realpath(__file__)) + os.sep + 'logs'
        if not os.path.exists(path):
            os.makedirs(path)

        self.r.set('ctime', time.time())
        self.r.set('is_report', 1)
        self.fds = []
        for arg in args:
            tname_Connect2txByIpaddr = 'Connect2txByIpaddr'
            ctime_Connect2txByIpaddr = time.time()
            res_Connect2txByIpaddr = Pysensor.Connect2txByIpaddr(*arg)
            self.record(tname_Connect2txByIpaddr, res_Connect2txByIpaddr[1], ctime_Connect2txByIpaddr, time.time())
            self.fds.append(res_Connect2txByIpaddr[0])
            self.fd_args[res_Connect2txByIpaddr[0]] = arg

        fd_list = []
        for fd in self.fds:
            if method == 'all':
                p1 = multiprocessing.Process(target=self.getMsg, args=(fd,))
                p2 = multiprocessing.Process(target=self.sendMsg, args=(fd,))

                p1.start()
                p2.start()

                fd_list.append((p1, p2))

            if method == 'get':
                p1 = multiprocessing.Process(target=self.getMsg, args=(fd,))
                p1.start()
                fd_list.append(p1)

            if method == 'send':
                p2 = multiprocessing.Process(target=self.sendMsg, args=(fd,))
                p2.start()
                fd_list.append(p2)

        # 测试报告
        report = Report.Report()
        p3 = multiprocessing.Process(target=report.report, args=())
        p3.start()
        p3.join()

        for p in fd_list:
            if method == 'all':
                p[0].join()
                p[1].join()
            if method == 'get' or method == 'send':
                p.join()

        print("main exit.")
        sys.exit(0)


if __name__ == '__main__':
    if len(sys.argv) <= 3:
        print('请输入传感器数量/配置文件/运行方式')
        print('eg: python Tianxun.py 10 config_file [all|get|send]')
        sys.exit(0)
    else:
        num = int(sys.argv[1])
        config = sys.argv[2]
        method = sys.argv[3]

        import_string = "from " + config + " import *"
        exec(import_string)

    tx = Tianxun()

    server_ip = SERVER_IP
    version = VERSION
    sn = SN
    client_port = ip.get_port(num, CLIENT_PORT)
    client_ip = ip.get_ip(CLIENT_IP)

    args = []
    for i in range(num):
        arg = [server_ip, client_ip.next(), client_port.next(), version, str(sn)]
        sn += 1
        args.append(arg)
    tx.main(method, args)
