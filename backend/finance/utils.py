import subprocess
import os
from finance.schema import Disk, Cpu, Memory
from typing import List
import wmi
import pythoncom


def run_cmd(cmd):
    p = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    stdout, stderr = p.stdout.decode('utf8'), p.stderr
    if p.returncode != 0:
        raise Exception(stdout + " " + stderr)
    return stdout


def ping_server(ip) -> bool:
    """测试服务器连接性

    :param ip:
    :return: bool
    """
    return not bool(os.system(f'ping -c 2 -t 1 {ip}'))


def download_file(ip, username, file, local_file):
    """下载文件到本地

    :param ip: 远程ip
    :param username: 远程用户名
    :param file: 远程文件名
    :param local_file: 本地文件名
    :return:
    """

    cmd = f'scp {local_file} {username}@{ip}:{file}'
    p = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    res = p.stdout.decode('utf8') + '\n' + p.stderr.decode('utf8')
    if p.returncode != 0:
        raise Exception(res)
    return res


def upload_file(ip, username, file, local_file):
    """上传文件到远程机器

    :param ip: 远程ip
    :param username: 远程用户名
    :param file: 远程文件名
    :param local_file: 本地文件
    :return:
    """

    cmd = f'scp {username}@{ip}:{file} {local_file}'
    return not bool(os.system(cmd))


def delete_file(file):
    """删除本地文件

    :param file:
    :return:
    """

    cmd = f'del {file}'
    p = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    res = p.stdout.decode('utf8') + '\n' + p.stderr.decode('utf8')
    if p.returncode != 0:
        raise Exception(res)
    return res


def delete_remote_file(ip, username, file):
    """删除远程文件

    :param ip:
    :param username:
    :param file:
    :return:
    """
    cmd = f'ssh {username}@{ip} "del {file}"'
    return not bool(os.system(cmd))


def list_local_cpu() -> List[Cpu]:
    pythoncom.Coinitialize()
    c = wmi.WMI()
    cpu_list = []

    for cpu in c.Win32_Processor():
        cpu_list.append(
            Cpu(
                name=cpu.Name,
                percent=cpu.LoadPercentage,
                core=cpu.NumberCores,
                speed=cpu.MaxClockSpeed,
            )
        )
    pythoncom.CoUninitialize()
    return cpu_list


def get_local_memory():
    pythoncom.Coinitialize()
    c = wmi.WMI()
    cs = c.Win32_ComputerSystem()
    os = c.Win32_OperatingSystem()
    pfu = c.Win32_PageFileUsage()

    total = int(cs[0].TotalPhysicalMemory)
    free = int(os[0].FreePhysicalMemory)
    pythoncom.CoUninitialize()

    return Memory(
        total=int(total / 1024 / 1024),
        free=int(free / 1024 / 1024),
        percent=int((total - free) / total * 100),
        swap_free=int(pfu[0].AllocatedBaseSize),
        swap_total=int(pfu[0].AllocatedBaseSize - pfu[0].CurrentUsage)
    )


def list_local_disk() -> List[Disk]:
    pythoncom.Coinitialize()
    c = wmi.WMI()
    disk_list = []

    for physical_disk in c.Win32_DiskDrive():
        for partition in physical_disk.associators("Win32_DiskDriveToDiskPartition"):
            for logical_disk in partition.associators("Win32_LogicalDiskToPartition"):
                total = int(logical_disk.Size)
                free = int(logical_disk.FreeSpace)

                disk_list.append(
                    Disk(
                        name=logical_disk.Caption,
                        total=int(total / 1024 / 1024 / 1024),
                        use=int((total - free) / 1024 / 1024 / 1024),
                        free=int(free / 1024 / 1024 / 1024),
                        percent=int((total - free) / total * 100)
                    )
                )
    pythoncom.CoUninitialize()
    return disk_list
