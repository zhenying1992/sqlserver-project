import json

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import JsonResponse

from query.model import UserPropertyModel


def loginView(request):
    data = json.loads(request.body)
    user = authenticate(
        username=data['username'],
        password=data['password']
    )
    if user is not None:
        login(request, user)
        resp = JsonResponse(data='登陆成功', status=200, safe=False)
        resp.set_cookie("username", user.username)
        resp.set_cookie("is_superuser", 1 if user.is_superuser else 0)
        return resp
    else:
        return JsonResponse(data='登陆失败', status=400, safe=False)


def logoutView(request):
    logout(request)
    resp = JsonResponse(data='退出成功', status=200, safe=False)
    resp.delete_cookie("username")
    resp.delete_cookie("is_superuser")
    return resp


def usersView(request):
    user_propertys = UserPropertyModel.objects.all()

    def get_user_property(name):
        for user_property in user_propertys:
            if user_property.username == name:
                return user_property
        return None

    users = User.objects.all()
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


def userView(request):
    if request.user.is_anonymous:
        user = {
            'username': None,
            'bms': [],
            'permissions': [],
            'isSuperUser': False
        }
        return JsonResponse(user, safe=False)

    user_property = UserPropertyModel.objects.filter(username=request.user.username).first()

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
        user = User.objects.create_user(username=username, password=password)
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
        user = User.objects.get(username=username)
        user.set_password(password)
        user.save()

    permissions = ','.join(permissions) if permissions else ""
    bms = ','.join(bms) if bms else ""
    user_property = UserPropertyModel.objects.filter(username=username).first()
    if user_property:
        user_property.permissions = permissions
        user_property.bms = bms
        user_property.save()
    else:
        UserPropertyModel.objects.create(
            username=username, permissions=permissions, bms=bms
        )

    return JsonResponse(data='success', safe=False)


def bmView(request):  # todo

    res = ['部门1', '部门2', '部门3']
    return JsonResponse(res, safe=False)


def xmView(request):  # todo

    res = ['项目1', '项目2', '项目3']
    return JsonResponse(res, safe=False)


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
    if request.user.is_anonymous:
        raise Exception("用户未登录")

    user_property = UserPropertyModel.objects.filter(username=request.user.username).first()
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

    print(xh, xm, bms, rxnd, sfnd, sfqf, current, page_size)
    # todo

    data = [{
        'XH': '123123',
        'XM': '张铁蛋',
        'KSH': '--',
        'SFZH': '122222',
        'RXND': '2000',
        'LXND': '2022',
        'BMDM': '1111',
        'BMMC': '部门名称11',
        'ZYDM': '2222',
        'ZYMC': '专业名称111',
        'SFQJDM': '12212',
        'SFQJMC': '收费区间名称111',
        'SFXMDM': '1111',
        'SFXMMC': '收费项目名称111',
        'YJJE': 100,
        'SJJE': 1,
        'TFJE': 2,
        'JMJE': 1,
        'HJJE': 1,
        'QFJE': 1
    }]
    res = {
        'total': 100,
        'current': 1,
        'pageSize': 10,
        'data': data
    }
    return JsonResponse(res, safe=False)


def zyColumnView(request):
    columns = [
        {'title': '年', 'key': 'nian', "width": 100},
        {'title': '月', 'key': 'yue', "width": 50},
        {'title': '学号', 'key': 'xh', "width": 100},
        {'title': '姓名', 'key': 'xm', "width": 100},
        {'title': '发放项目名称', 'key': 'ffxmdm', "width": 200},
        {'title': '摘要', 'key': 'zy', "width": 100},
        {'title': '应发金额', 'key': 'je', "width": 100},
        {'title': '税额', 'key': 'se', "width": 150},
        {'title': '税率', 'key': 'sl', "width": 100},
        {'title': '实发金额', 'key': 'sfje', "width": 150},
        {'title': '部门编号', 'key': 'bmbh', "width": 150},
        {'title': '项目编号', 'key': 'xmbh', "width": 150},
    ]
    return JsonResponse(columns, safe=False)


def zyDataView(request):
    if request.user.is_anonymous:
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
    print(xh, bmbh, xmbh, ffny_start, ffny_end, ffxm, current, page_size)
    # todo
    data = [{
        'nian': '2022',
        'yue': '2',
        'xh': '122222',
        'xm': '姓名',
        'ffxmdm': '2000',
        'zy': '摘要',
        'je': '1111',
        'se': '11',
        'sl': '11',
        'sfje': '11',
        'bmbh': '111',
        'xmbh': '收费区间名称111',
    }]
    res = {
        'total': 10,
        'current': 1,
        'pageSize': 10,
        'data': data
    }
    return JsonResponse(res, safe=False)
