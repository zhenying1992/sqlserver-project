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

function getDataApi(xh, xm, bm, rxnd, sfnd, sfqf, pagination) {
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

function getZyDataApi(xh, bmbh, xmbh, ffnyStart, ffnyEnd, ffxm, pagination) {
    return client.get("/zy/data", {
        params: {
            'xh': xh,
            'bmbh': bmbh,
            'xmbh': xmbh,
            'ffnyStart': ffnyStart,
            'ffnyEnd': ffnyEnd,
            'ffxm': ffxm,
            'current': pagination.current,
            'pageSize': pagination.pageSize,
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