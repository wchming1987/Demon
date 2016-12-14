#!/usr/bin/env python
# -*- coding=utf-8 -*-

import datetime
import sys

import psutil

type = sys.getfilesystemencoding()

class SystemMoniter():
    ## CPU 信息
    cpu = {
        # CPU 品牌型号
        'cpu_name': '',
        # CPU 核心
        'cpu_core': {
            # 物理核心数量
            'physical_core': 0,
            # 逻辑核心数量
            'logic_core': 0
        },
        # CPU 状态
        'cpu_status': {
            'ctx_switches': 0,
            'interrupts': 0,
            'soft_interrupts': 0,
            'sys_calls': 0
        },
        # CPU 利用率
        'cpu_times': {
            # 执行用户进程的时间比
            'user': 0,
            # 执行内核进程和终端的时间百分比
            'system': 0,
            # CPU 处于 IDLE 状态的时间百分比
            'idle': 0,
            'percent': 0
        }
    }
    mem = {'total' : 0, 'avaiable' : 0, 'percent' : 0, 'used' : 0, 'free' : 0}

    #磁盘名称
    disk_id = []
    #将每个磁盘的total used free percent 分别存入到相应的list
    disk_total = []
    disk_used = []
    disk_free = []
    disk_percent = []

    ## 网络信息
    network = {
        'nics': {
            'mac': '',
            'ip_address': '',
            'netmask': '',
            'broadcast': ''
        }
    }

    ## 获取CPU信息
    def get_cpu_info(self):

        # 获取 CPU 核心数量
        self.cpu['cpu_core']['physical_core'] = psutil.cpu_count(logical=False)
        self.cpu['cpu_core']['logic_core'] = psutil.cpu_count(logical=True)

        # 获取 CPU 利用率
        cpu_times = psutil.cpu_times()
        self.cpu['cpu_times']['user'] = cpu_times.user
        self.cpu['cpu_times']['system'] = cpu_times.system
        self.cpu['cpu_times']['idle'] = cpu_times.idle
        self.cpu['cpu_times']['percent'] = psutil.cpu_percent(interval=2)

    ## 获取内存信息
    def get_mem_info(self):
        mem_info = psutil.virtual_memory()
        self.mem['total'] = mem_info.total
        self.mem['available'] = mem_info.available
        self.mem['percent'] = mem_info.percent
        self.mem['used'] = mem_info.used
        self.mem['free'] = mem_info.free

    ## 获取磁盘信息
    def get_disk_info(self):
        for id in psutil.disk_partitions():
            if 'cdrom' in id.opts or id.fstype == '':
                continue
            disk_name = id.device.split(':')
            s = disk_name[0]
            self.disk_id.append(s)
            disk_info = psutil.disk_usage(id.device)
            self.disk_total.append(disk_info.total)
            self.disk_used.append(disk_info.used)
            self.disk_free.append(disk_info.free)
            self.disk_percent.append(disk_info.percent)

    ## 获取网络信息
    def get_netowrk_info(self):
        nics = psutil.net_if_stats()
        print nics
        for (k, v) in nics.items():
            print v
            self.network[k] = {}
            self.network[k]['isUp'] = v.isup
            self.network[k]['duplex'] = v.duplex
            self.network[k]['speed'] = v.speed
            self.network[k]['mtu'] = v.mtu
            print k, self.network[k]

        nics = psutil.net_if_addrs()
        for (k, v) in nics.items():
            print k.decode(type).encode('utf-8')
            print v
            for nic in v:
                # MAC 地址
                if nic.family == -1:
                    print 'MAC 地址:[%s]' % nic.address
                elif nic.family == 2:
                    print 'IP 地址:[%s]' % nic.address
                    print '子网掩码:[%s]' % nic.netmask
                    print '广播地址:[%s]' % nic.broadcast

        net = psutil.net_io_counters()
        bytes_sent = '{0:.2f} kb'.format(net.bytes_recv / 1024)
        bytes_rcvd = '{0:.2f} kb'.format(net.bytes_sent / 1024)
        print u"网卡接收流量 %s 网卡发送流量 %s" % (bytes_rcvd, bytes_sent)

    ## 获取系统信息
    def get_system_info(self):
        print u"系统启动时间 %s" % datetime.datetime.fromtimestamp(psutil.boot_time()).strftime("%Y-%m-%d %H:%M:%S")

    ## 获取用户信息
    def get_user_info(self):
        users = psutil.users()
        user_count = len(users)
        user_list = ','.join([ u.name for u in psutil.users()])
        print u"当前有%d个用户，分别是%s" % (user_count, user_list)


if __name__ == '__main__':
    moniter = SystemMoniter()

    #moniter.get_cpu_info()
    #moniter.get_mem_info()
    #moniter.get_disk_info()
    moniter.get_netowrk_info()
    #moniter.get_system_info()
    ##moniter.get_user_info()
