import csv

import json

from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.hashers import check_password

from query.db import xf_query, zy_query, list_bm, list_xm
from query.model import UserPropertyModel
import uuid


def loginView(request):
    data = json.loads(request.body)

    user = User.objects.using('query').filter(username=data['username']).all()
    if not user:
        return JsonResponse(data='不存在用户', status=400, safe=False)

    user = user[0]
    if check_password(data['password'], user.password):
        key = uuid.uuid4()
        user.first_name = key
        user.save()
        resp = JsonResponse(data='登陆成功', status=200, safe=False)
        resp.set_cookie('session_key', key)
        resp.set_cookie("username", user.username)
        resp.set_cookie("is_superuser", 1 if user.is_superuser else 0)
        return resp
    else:
        return JsonResponse(data='密码错误', status=400, safe=False)


def logoutView(request):
    logout(request)
    resp = JsonResponse(data='退出成功', status=200, safe=False)
    resp.delete_cookie("session_key")
    resp.delete_cookie("username")
    resp.delete_cookie("is_superuser")
    return resp


def usersView(request):
    user_propertys = UserPropertyModel.objects.using('query').all()

    def get_user_property(name):
        for user_property in user_propertys:
            if user_property.username == name:
                return user_property
        return None

    users = User.objects.using('query').all()
    res = []
    for item in users:
        user_property = get_user_property(item.username)
        user = {
            'username': item.username,
            'lastLogin': item.last_login.strftime("%Y-%m-%d %H:%M:%S") if item.last_login else "",
            'isSuperUser': "是" if item.is_superuser else "否",
            'bms': user_property.bms if user_property else "",
            'permissions': user_property.permissions if user_property else "",
        }
        res.append(user)

    return JsonResponse(res, safe=False)


def get_user(request):
    session_key = request.COOKIES.get("session_key")
    users = User.objects.using('query').all()
    for user in users:
        if user.first_name == session_key:
            request.user = user
            return user

    return None


def userView(request):
    get_user(request)
    if request.user.is_anonymous:
        user = {
            'username': None,
            'bms': [],
            'permissions': [],
            'isSuperUser': False
        }
        return JsonResponse(user, safe=False)

    user_property = UserPropertyModel.objects.using('query').filter(username=request.user.username).first()

    user = {
        'username': request.user.username,
        'bms': user_property.bms.split(",") if user_property else [],
        'permissions': user_property.permissions.split(',') if user_property else [],
        'isSuperUser': request.user.is_superuser
    }
    return JsonResponse(user, safe=False)


def createView(request):
    data = json.loads(request.body)
    username = data['username']
    password = data['password']
    try:
        user = User.objects.using('query').create_user(username=username, password=password)
        user.save()
    except Exception as ex:
        return JsonResponse(data=str(ex), status=400, safe=False)

    return JsonResponse(data='success', safe=False)


def updateView(request):
    data = json.loads(request.body)
    username = data['username']
    password = data['password']
    permissions = data['permissions']
    bms = data['bms']

    if password:
        user = User.objects.using('query').get(username=username)
        user.set_password(password)
        user.save()

    permissions = ','.join(permissions) if permissions else ""
    bms = ','.join(bms) if bms else ""
    user_property = UserPropertyModel.objects.using('query').filter(username=username).first()
    if user_property:
        user_property.permissions = permissions
        user_property.bms = bms
        user_property.save()
    else:
        UserPropertyModel.objects.using('query').create(
            username=username, permissions=permissions, bms=bms
        )

    return JsonResponse(data='success', safe=False)


def bmView(request):
    # return JsonResponse([], safe=False)
    return JsonResponse(list_bm(), safe=False)


def xmView(request):
    # return JsonResponse([], safe=False)
    return JsonResponse(list_xm(), safe=False)


def columnView(request):
    columns = [
        {'title': '学号', 'key': 'XH', "width": 100},
        {'title': '姓名', 'key': 'XM', "width": 100},
        {'title': 'KSH', 'key': 'KSH', "width": 100},
        {'title': '身份证号', 'key': 'SFZH', "width": 200},
        {'title': '入学年度', 'key': 'RXND', "width": 100},
        {'title': '离校年度', 'key': 'LXND', "width": 100},
        {'title': '部门代码', 'key': 'BMDM', "width": 100},
        {'title': '部门名称', 'key': 'BMMC', "width": 150},
        {'title': '专业代码', 'key': 'ZYDM', "width": 100},
        {'title': '专业名称', 'key': 'ZYMC', "width": 150},
        {'title': '收费区间代码', 'key': 'SFQJDM', "width": 150},
        {'title': '收费区间名称', 'key': 'SFQJMC', "width": 150},
        {'title': '收费项目代码', 'key': 'SFXMDM', "width": 150},
        {'title': '收费项目名称', 'key': 'SFXMMC', "width": 150},
        {'title': '应缴金额', 'key': 'YJJE', "width": 100},
        {'title': '实缴金额', 'key': 'SJJE', "width": 100},
        {'title': '退费金额', 'key': 'TFJE', "width": 100},
        {'title': '减免金额', 'key': 'JMJE', "width": 100},
        {'title': 'HJJE', 'key': 'HJJE', "width": 100},
        {'title': '欠费金额', 'key': 'QFJE', "width": 100},
    ]
    return JsonResponse(columns, safe=False)


def dataView(request):
    user = get_user(request)

    if not user:
        raise Exception("用户未登录")

    user_property = UserPropertyModel.objects.using('query').filter(username=request.user.username).first()
    if not user_property or user_property.bms == '':
        raise Exception("用户没有部门权限")

    user_bms = user_property.bms.split(',')

    params = request.GET
    xh = params.get("xh")
    xm = params.get("xm")
    bm = params.get('bm')
    if bm:
        if bm not in user_bms:
            raise Exception(f"没有部门{bm}的权限")
        bms = [bm]
    else:
        bms = user_bms
    rxnd = params.get('rxnd')
    sfnd = params.get('sfnd')
    sfqf = params.get('sfqf')
    current = params.get('current', 1)
    page_size = params.get('pageSize', 10)

    is_download = params.get("isDownload", False)

    # print(xh, xm, bms, rxnd, sfnd, sfqf, current, page_size)
    data, total = xf_query(xh, xm, bms, rxnd, sfnd, sfqf, current, page_size)

    # data = [{
    #     'XH': '123123',
    #     'XM': '张铁蛋',
    #     'KSH': '--',
    #     'SFZH': '122222',
    #     'RXND': '2000',
    #     'LXND': '2022',
    #     'BMDM': '1111',
    #     'BMMC': '部门名称11',
    #     'ZYDM': '2222',
    #     'ZYMC': '专业名称111',
    #     'SFQJDM': '12212',
    #     'SFQJMC': '收费区间名称111',
    #     'SFXMDM': '1111',
    #     'SFXMMC': '收费项目名称111',
    #     'YJJE': 100,
    #     'SJJE': 1,
    #     'TFJE': 2,
    #     'JMJE': 1,
    #     'HJJE': 1,
    #     'QFJE': 1
    # }]
    # total = 11
    if is_download:
        header = ['XH', 'XM', 'KSH', 'SFZH', 'RXND', 'LXND', 'BMDM', 'BMMC', 'ZYDM', 'ZYMC', 'SFQJDM',
                  'SFQJMC', 'SFXMDM', 'SFXMMC', 'YJJE', 'SJJE', 'TFJE', 'JMJE', 'HJJE', 'QFJE']
        response = HttpResponse()
        response['Content-Disposition'] = 'attachment; filename="xf_data.csv"'
        response['Content-Type'] = 'text/csv'
        response['charset'] = 'utf-8-sig'
        writer = csv.DictWriter(response, fieldnames=header)
        writer.writeheader()
        for item in data:
            writer.writerow(item)

        return response

    res = {
        'total': total,
        'current': current,
        'pageSize': page_size,
        'data': data
    }
    return JsonResponse(res, safe=False)


def zyColumnView(request):
    columns = [
        {'title': '年', 'key': 'nian', "width": 100},
        {'title': '月', 'key': 'yue', "width": 100},
        {'title': '学号', 'key': 'xh', "width": 100},
        {'title': '姓名', 'key': 'xm', "width": 100},
        # {'title': '发放项目名称', 'key': 'ffxmdm', "width": 200},
        {'title': '摘要', 'key': 'zy', "width": 400},
        {'title': '应发金额', 'key': 'je', "width": 100},
        {'title': '税额', 'key': 'se', "width": 150},
        {'title': '税率', 'key': 'sl', "width": 100},
        {'title': '实发金额', 'key': 'sfje', "width": 150},
        {'title': '部门编号', 'key': 'bmbh', "width": 150},
        {'title': '项目编号', 'key': 'xmbh', "width": 150},
    ]
    return JsonResponse(columns, safe=False)


def zyDataView(request):
    user = get_user(request)
    if not user:
        raise Exception("用户未登录")

    params = request.GET
    xh = params.get("xh")
    bmbh = params.get("bmbh")
    xmbh = params.get('xmbh')
    ffny_start = params.get('ffnyStart')
    ffny_end = params.get('ffnyEnd')
    ffxm = params.get('ffxm')
    current = params.get('current', 1)
    page_size = params.get('pageSize', 10)

    is_download = params.get('isDownload', False)
    # print(xh, bmbh, xmbh, ffny_start, ffny_end, ffxm, current, page_size)

    data, total = zy_query(xh, bmbh, xmbh, ffxm, current, page_size)
    # data = [{
    #     'nian': '2022',
    #     'yue': '2',
    #     'xh': '122222',
    #     'xm': '姓名',
    #     'zy': '摘要',
    #     'je': '1111',
    #     'se': '11',
    #     'sl': '11',
    #     'sfje': '11',
    #     'bmbh': '111',
    #     'xmbh': '收费区间名称111',
    # } for i in range(1,10)]
    # total = 11
    if is_download:
        header = ['nian', 'yue', 'xh', 'xm', 'zy', 'je', 'se', 'sl', 'sfje', 'bmbh', 'xmbh']
        response = HttpResponse()
        response['Content-Disposition'] = 'attachment; filename="zy_data.csv"'
        response['Content-Type'] = 'text/csv'
        response['charset'] = 'utf-8-sig'
        writer = csv.DictWriter(response, fieldnames=header)
        writer.writeheader()
        for item in data:
            writer.writerow(item)

        return response

    res = {
        'total': total,
        'current': current,
        'pageSize': page_size,
        'data': data
    }
    return JsonResponse(res, safe=False)
