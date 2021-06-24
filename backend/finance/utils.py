import subprocess
import os


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
