import axios from "axios";
import ViewUI from "view-ui-plus/dist/viewuiplus.min.esm";

const client = axios.create({
    baseURL: '/query/api',
    timeout: 5000,
    withCredentials: true,
    headers: {
        'Content-Type': "application/json",
    }
})

client.interceptors.response.use(
    function (response) {
        return response.data
    },
    function (error) {
        ViewUI.Message.error({content: "后端服务器请求失败:" + error.response.data, duration: 5})
        return 'failed'
    }
)


function listUserApi() {
    return client.get("/users")
}

function getUserApi() {
    return client.post("/user")
}

function createUserApi(username, password) {
    return client.post("/create-user", {"username": username, "password": password})
}

function editUserApi(username, password, bms, permissions) {
    return client.post("/update-user",
        {"username": username, "password": password, "bms": bms, "permissions": permissions}
    )
}

function loginApi(username, password) {
    return client.post("/login", {"username": username, "password": password})
}

function logoutApi() {
    return client.post("/logout")
}

function listBmApi() {
    return client.get("/bm")
}

function listXmApi() {
    return client.get("/xm")
}

function getColumnApi() {
    return client.get("/column")
}

function getDataApi(xh, xm, bm, rxnd, sfnd, sfqf, pagination, isDownload) {
    if (isDownload) {
        return axios.get('/query/api/data', {
            params: {
                'xh': xh,
                'xm': xm,
                'bm': bm,
                'rxnd': rxnd,
                'sfnd': sfnd,
                'sfqf': sfqf,
                'current': pagination.current,
                'pageSize': pagination.pageSize,
                'isDownload': isDownload
            },
            responseType: 'blob'  // 设置响应类型为二进制数据
        }).then(response => {
            const url = URL.createObjectURL(new Blob([response.data]));  // 创建临时下载链接
            const link = document.createElement('a');  // 创建a标签
            link.href = url;  // 设置a标签的href属性为下载链接
            link.download = 'data.csv';  // 设置下载文件的文件名
            link.click();  // 触发a标签的点击事件进行下载
        });
    }
    return client.get("/data",
        {
            params: {
                'xh': xh,
                'xm': xm,
                'bm': bm,
                'rxnd': rxnd,
                'sfnd': sfnd,
                'sfqf': sfqf,
                'current': pagination.current,
                'pageSize': pagination.pageSize,
            }
        }
    )
}

function getZyColumnApi() {
    return client.get("/zy/column")
}

function getZyDataApi(xh, bmbh, xmbh, ffnyStart, ffnyEnd, ffxmdm, pagination, isDownload) {
    if (isDownload) {
        return axios.get('/query/api/zy/data', {
            params: {
                'xh': xh,
                'bmbh': bmbh,
                'xmbh': xmbh,
                'ffnyStart': ffnyStart,
                'ffnyEnd': ffnyEnd,
                'ffxmdm': ffxmdm,
                'current': pagination.current,
                'pageSize': pagination.pageSize,
                'isDownload': isDownload
            },
            responseType: 'blob'  // 设置响应类型为二进制数据
        }).then(response => {
            const url = URL.createObjectURL(new Blob([response.data]));  // 创建临时下载链接
            const link = document.createElement('a');  // 创建a标签
            link.href = url;  // 设置a标签的href属性为下载链接
            link.download = 'zy_data.csv';  // 设置下载文件的文件名
            link.click();  // 触发a标签的点击事件进行下载
        });
    }

    return client.get("/zy/data", {
        params: {
            'xh': xh,
            'bmbh': bmbh,
            'xmbh': xmbh,
            'ffnyStart': ffnyStart,
            'ffnyEnd': ffnyEnd,
            'ffxmdm': ffxmdm,
            'current': pagination.current,
            'pageSize': pagination.pageSize,
            'isDownload': isDownload
        }
    })
}

export {
    getUserApi,
    listUserApi,
    createUserApi,
    editUserApi,
    loginApi,
    logoutApi,

    listBmApi,
    listXmApi,
    getColumnApi,
    getDataApi,
    getZyColumnApi,
    getZyDataApi
}