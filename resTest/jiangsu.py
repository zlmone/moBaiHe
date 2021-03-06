# coding=utf-8

import time
import uiautomator2 as u2
import os
import xlwt

# 程序注意事项：
# 1，需要先点击视频播放，本次选取“神奇动物在哪里”片源，需要先点击视频播放，本次选取“神奇动物在哪里”片源
# 2，然后执行本程序，执行前可以调整参数
# 被测设备的IP地址
IP_ADDRESS = "192.168.1.149"
CITY_NAME = '江苏'
WAIT_TIME = 10
TEST_COUNTS = 180

class JiangSuPerformance:
    def __init__(self, d):
        self.d = d
    def getMacAddress(self):
        command = "adb shell cat /sys/class/net/eth0/address"
        output = os.popen(command)
        for line in output:
            return line
    # 获取被测设备的内存总量，执行1次
    def getTotalRAM(self):
        print("获取魔百和内存总量，单位KB")
        command = "adb shell dumpsys meminfo"
        output = os.popen(command)
        totalRAM = 0
        for line in output.readlines():
            if "Total RAM:" in line:
                print(line)
                totalRAM = line.split()[2]
                return totalRAM

    # 获取被测设备当前内存使用情况
    def getUsedRAM(self):
        print("获取魔百和业务运行内存使用，单位KB")
        ram = 0
        command = "adb shell dumpsys meminfo"
        output = os.popen(command)
        # i = 1
        for line in output.readlines():
            if "Used RAM:" in line:
                print(line)
                ram = line.split()[2]
                # print(ramTemp)
                return ram

def timeStyle(timestamp):
    time_Now = int(timestamp)
    time_local = time.localtime(time_Now)
    dt = time.strftime("%Y-%m-%d %H-%M-%S", time_local)
    return dt


if __name__ == '__main__':
    jiangsuTestCase1 = JiangSuPerformance(u2.connect(IP_ADDRESS))
    jiangsuTotalRAM = int(jiangsuTestCase1.getTotalRAM()) / 1024
    jiangsuMacAddress = jiangsuTestCase1.getMacAddress()
    #  创建一个工作薄
    book = xlwt.Workbook(encoding='utf-8', style_compression=0)
    # 添加一个sheet，命名为“RAM”，参数cell_overwrite_ok为True表示可以重复输入
    sheet = book.add_sheet(CITY_NAME+"RAM", cell_overwrite_ok=True)

    sheet.write(0, 0, '轮次')
    sheet.write(0, 1, 'RAM（MB）')
    sheet.write(0, 2, '时间')
    sheet.write(0, 3, 'TOTAL_RAM:' + str(jiangsuTotalRAM) + "MB")
    sheet.write(0, 4, 'IP:' + IP_ADDRESS)
    sheet.write(0, 5,'MacAddress'+ jiangsuMacAddress)
    timeTemp = timeStyle(time.time())
    print(timeTemp)

    print("魔百和RAM大小为：" + str(jiangsuTotalRAM) + "MB")
    # 执行30分钟，每30s记录一次数据，共记录60组数据。
    k = 1
    while k < TEST_COUNTS + 1:
        st = time.time()
        jiangsuUsedRAMTemp = int(jiangsuTestCase1.getUsedRAM()) / 1024
        sheet.write(k, 0, k)
        sheet.write(k, 1, str(jiangsuUsedRAMTemp))
        sheet.write(k, 2, str(timeStyle(st)))
        if WAIT_TIME:
            waitTimeTemp = WAIT_TIME - (time.time() - st)
            time.sleep(waitTimeTemp)
        # myeddut = time.time() - st
        k += 1
    book.save('./updateResult'+ CITY_NAME + str(timeTemp) + '.xls')