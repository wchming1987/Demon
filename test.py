#!/usr/bin/env python
# -*- coding=utf-8 -*-

import psutil

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

#获取CPU信息
def get_cpu_info():

    # 获取 CPU 核心数量
    cpu['cpu_core']['physical_core'] = psutil.cpu_count(logical=False)
    cpu['cpu_core']['logic_core'] = psutil.cpu_count(logical=True)

    # 获取 CPU 利用率
    cpu_times = psutil.cpu_times()
    cpu['cpu_times']['user'] = cpu_times.user
    cpu['cpu_times']['system'] = cpu_times.system
    cpu['cpu_times']['idle'] = cpu_times.idle
    cpu['cpu_times']['percent'] = psutil.cpu_percent(interval=2)

#获取内存信息
def get_mem_info():
    mem_info = psutil.virtual_memory()
    mem['total'] = mem_info.total
    mem['available'] = mem_info.available
    mem['percent'] = mem_info.percent
    mem['used'] = mem_info.used
    mem['free'] = mem_info.free

#获取磁盘
def get_disk_info():
    for id in psutil.disk_partitions():
        if 'cdrom' in id.opts or id.fstype == '':
            continue
        disk_name = id.device.split(':')
        s = disk_name[0]
        disk_id.append(s)
        disk_info = psutil.disk_usage(id.device)
        disk_total.append(disk_info.total)
        disk_used.append(disk_info.used)
        disk_free.append(disk_info.free)
        disk_percent.append(disk_info.percent)


if __name__ == '__main__':
    get_cpu_info()
    print u"CPU信息: %s" % cpu
    get_mem_info()
    mem_status = mem['percent']
    print u"内存使用率: %s %%" % mem_status
    get_disk_info()
    for i in range(len(disk_id)):
        print u'%s盘空闲率: %s %%' % (disk_id[i],100 - disk_percent[i])
    raw_input("Enter enter key to exit...")
