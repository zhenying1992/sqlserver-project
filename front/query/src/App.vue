<style scoped>
.layout {
  border: 1px solid #d7dde4;
  background: #f5f7f9;
  position: relative;
  border-radius: 4px;
  overflow: hidden;
  height: 100%;
}

.layout-footer-center {
  text-align: center;
}
</style>

<template>
  <div class="layout">
    <Layout style="min-height: 100vh">
      <Header>
        <Menu mode="horizontal" theme="dark">
          <div style="color: #d7dde4; font-size: 30px; float: left">查询系统</div>
          <div style="color: #d7dde4; float: right">
            <Dropdown v-if="this.user.username" @on-click="click">
              <a href="javascript:void(0)">
                {{ this.user.username }}
                <Icon type="ios-arrow-down"></Icon>
              </a>
              <template #list>
                <DropdownMenu>
                  <DropdownItem name="logout">退出</DropdownItem>
                </DropdownMenu>
              </template>
            </Dropdown>
            <Button v-else type="text" style="color: #d7dde4" @click="showLogin=true">登录</Button>

          </div>
        </Menu>
      </Header>
      <Layout :style="{padding: '0 50px'}">
        <Content :style="{padding: '24px 0', minHeight: '280px', background: '#fff'}">
          <Layout>
            <Sider hide-trigger :style="{background: '#fff'}">
              <Menu active-name="query" theme="light" width="auto" :open-names="['1']" @on-select="change">
                <MenuItem name="query" v-if="hasQueryPermission">学费查询</MenuItem>
                <MenuItem name="queryZy" v-if="hasQueryZyPermission">助研费查询</MenuItem>
                <MenuItem name="user" v-if="this.user.isSuperUser">用户管理</MenuItem>
              </Menu>
            </Sider>
            <Content :style="{padding: '24px', minHeight: '280px', background: '#fff'}">
              <Query v-if="showModule==='query'"></Query>
              <QueryZy v-if="showModule==='queryZy'"></QueryZy>
              <User v-if="showModule==='user'"></User>
            </Content>
          </Layout>
        </Content>
      </Layout>
      <Footer class="layout-footer-center">2011-2016 &copy; View Design</Footer>
    </Layout>

    <Modal
        v-model="showLogin"
        title="登录"
        @on-ok="login"
        width="400px"
    >
      <div>
        <span>用户名</span>
        <Input v-model="username" placeholder="请输入用户名" style="width: 200px; margin-left: 10px"></Input>
      </div>
      <div style="margin-top: 10px">
        <span style="margin-left: 13px">密码</span>
        <Input type="password" v-model="password" placeholder="请输入密码"
               style="width: 200px; margin-left: 10px"></Input>
      </div>
    </Modal>
  </div>
</template>
<script>
import User from "./components/User.vue";
import Query from "./components/Query.vue";
import QueryZy from "./components/QueryZy.vue";
import {getUserApi, loginApi, logoutApi} from "./api/query";

export default {
  components: {Query, User, QueryZy},
  data() {
    return {
      showModule: "query",
      showLogin: false,
      username: '',
      password: '',
      user: {
        isSuperUser: false,
        permissions: [],
        bms: []
      }
    }
  },
  created() {
    this.getUser()
  },
  computed: {
    hasQueryPermission: function() {
      return this.user.permissions.includes('学费查询')
    },
    hasQueryZyPermission: function() {
      return this.user.permissions.includes('助研费查询')
    }
  },
  methods: {
    change(value) {
      this.showModule = value
    },
    async getUser() {
      this.user = await getUserApi()
    },
    async login() {
      let res = await loginApi(this.username, this.password)
      if (res !== 'failed') {
        window.location.reload()
      }
    },
    async click(v) {
      await logoutApi()
      window.location.reload()
    }
  }
}
</script>
