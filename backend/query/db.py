import pymssql


class Transaction:
    def __init__(self):  # todo
        self.host = ''
        self.port = ''
        self.db = ''
        self.user = ''
        self.password = ''

    def __call__(self, *args, **kwargs):
        def wrap(fn):
            with self:
                return fn(*args, **kwargs)

        return wrap

    def __enter__(self):
        self.conn = pymssql.connect(
            host=self.host,
            port=self.port,
            user=self.user,
            password=self.password,
            database=self.db
        )
        self.cursor = self.conn.cursor()
        return self.cursor

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.cursor:
            self.cursor.close()

        if self.conn:
            self.conn.close()


def list_bm():
    with Transaction() as cursor:
        cursor.execute("select BMMC from PBMDM")
        res = cursor.fetchall()
        return [item[0] for item in res]


def list_xm():
    with Transaction() as cursor:
        cursor.execute("select id, xmmc from xs_zyfxmdm")
        res = []
        for item in cursor.fetchall():
            res.append({
                'id': item[0],
                'name': item[1]
            })
        return res


def xf_query(xh=None, xm=None, bms=None, rxnd=None, sfnd=None, sfqf=None, current=1, page_size=10):
    with Transaction() as cursor:
        sql = "select XH, XM, RXND, LXNX, BMDM, BMMC, ZYDM, ZYMC," \
              "SFQJDM, SFQJMC, SFXMDM, SFXMMC, YJJE, SJJE, TFJE, JMJE, HJJE, QFJE " \
              "from datazz"

        where = ''
        if xh:
            where += f' XH="{xh}" '

        if xm:
            where += f' XM="{xm}" '

        if bms:
            bms = '","'.join(bms)
            where += f' BMMC in "{bms}" '

        if rxnd:
            where += f' RXND="{rxnd}" '

        if sfnd:
            where += f' SFND="{sfnd}" '

        if sfqf:
            where += f' SFQF={sfqf}'

        if where:
            sql = f'{sql} where {where} limit {current}, {page_size}'

        cursor.execute(f"select count(1) from datazz where {where}")
        res = cursor.fetchall()
        total = res[0][0]

        cursor.execute(sql)
        res = cursor.fetchall()
        return [
            {
                'nian': item[0],
            }
            for item in res
        ], total


def zy_query(xh, bmbh, xmbh, ffxmdm, ffny_start, ffny_end, current=1, page_size=10):
    with Transaction() as cursor:
        sql = "select nian, yue, xh, xm, zy, je, se, sl, sfje, bmbh, xmbh from xs_zyffb"
        where = ''
        if xh:
            where += f' xh="{xh}"'

        if bmbh:
            where += f' bmbh="{bmbh}"'

        if xmbh:
            where += f' xmbh="{xmbh}"'

        if ffxmdm:
            where += f' ffxmdm="{ffxmdm}"'

        if ffny_start:
            where += f' nian>="{ffny_start}"'

        if ffny_end:
            where += f' ffny<="{ffny_end}"'

        if where:
            sql = f'{sql} where {where} limit {current}, {page_size}'

        cursor.execute(f"select count(1) from datazz where {where}")
        res = cursor.fetchall()
        total = res[0][0]

        cursor.execute(sql)
        res = cursor.fetchall()
        return [
            {
                'nian': item[0],
                'yue': item[1],
                'xh': item[2],
                'xm': item[3],
                'ffxmd': item[4],
                'zy': item[5],
                'je': item[6],
                'se': item[7],
                'sl': item[8],
                'sfje': item[9],
                'bmbh': item[10],
                'xmbh': item[11],
            }
            for item in res
        ], total
