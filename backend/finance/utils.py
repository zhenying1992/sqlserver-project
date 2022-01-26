import subprocess
import os
import datetime
from finance.schema import Disk, Cpu, Memory, Sys
from typing import List
import wmi
import pythoncom
import pymssql


def run_cmd(cmd):
    print(cmd)
    ret = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    print(ret.stdout.decode('gbk'))
    print(ret.stderr.decode('gbk'))
    return ret.returncode == 0


def ping_server(ip) -> bool:
    """测试服务器连接性

    :param ip:
    :return: bool
    """
    return not bool(os.system(f'ping -n 2 -w 1000 {ip}'))


def ping_sqlserver(ip, dbuser, password):
    try:
        return pymssql.connect(host=ip, user=dbuser, password=password)
    except Exception:
        return False


def backup_sqlserver(ip, username, password, database, local_path):
    cmd = fr"net use \\{ip}\ipc$ {password} /user:{username} "
    cmd1 = f"sqlcmd -s . -E -Q \"BACKUP DATABASE {database} TO DISK='{local_path}'\""
    run_cmd(cmd)
    run_cmd(cmd1)
    return True


def copy_file(ip, dest_path, local_path, username, password) -> bool:
    cmd2 = fr"net use \\{ip}\ipc$ {password} /user:{username} "
    cmd3 = fr"Xcopy \\{ip}{dest_path} {local_path} /s /e /y /d"
    run_cmd(cmd2)
    run_cmd(cmd3)
    return True


def delete_local_file(local_path, days=30):
    cmd = f'forfiles /p "{local_path}" /m *.bak /d -{days} /c "cmd /c del @path"'
    return run_cmd(cmd)


def delete_dest_file(ip, dest_path):
    cmd = ''
    return run_cmd(cmd)


def list_local_cpu() -> List[Cpu]:
    pythoncom.CoInitialize()
    c = wmi.WMI()
    cpu_list = []

    for cpu in c.Win32_Processor():
        cpu_list.append(
            Cpu(
                name=cpu.Name,
                percent=cpu.LoadPercentage,
                core=cpu.NumberOfCores,
                speed=cpu.MaxClockSpeed,
            )
        )
    pythoncom.CoUninitialize()
    return cpu_list


def get_local_memory():
    pythoncom.CoInitialize()
    c = wmi.WMI()
    cs = c.Win32_ComputerSystem()
    os = c.Win32_OperatingSystem()
    pfu = c.Win32_PageFileUsage()

    total = int(cs[0].TotalPhysicalMemory) / 1024 / 1024
    free = int(os[0].FreePhysicalMemory) / 1024
    pythoncom.CoUninitialize()

    return Memory(
        total=int(total),
        free=int(free),
        percent=int((total - free) / total * 100),
        swap_free=int(pfu[0].AllocatedBaseSize),
        swap_total=int(pfu[0].AllocatedBaseSize - pfu[0].CurrentUsage)
    )


def list_local_disk() -> List[Disk]:
    pythoncom.CoInitialize()
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


def get_sys_info():
    pythoncom.CoInitialize()
    c = wmi.WMI()
    sys = c.Win32_OperatingSystem()

    process = sys[0].NumberOfProcesses
    last_up_time = datetime.datetime.strptime(sys[0].LastBootupTime[:14], "%Y%m%d%H%M%S")
    uptime = datetime.datetime.now() - last_up_time

    pythoncom.CoUninitialize()
    return Sys(
        process=process,
        uptime=str(uptime)
    )
