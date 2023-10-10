<template>
  <div>
    <Button type="primary" @click="show_create=true">新建用户</Button>
    <Table :columns="columns" :data="users" style="margin-top: 10px">
      <template #action="{ row, index }">
        <Button type="primary" size="small" style="margin-right: 5px" @click="onEdit(row.username)">编辑</Button>
      </template>
    </Table>

    <Modal
        v-model="show_create"
        title="新建用户"
        @on-ok="create"
        width="300px"
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

    <Modal
        v-model="show_edit"
        title="编辑用户"
        @on-ok="edit"
        width="400px">
      <div>
        <span>密码</span>
        <Input v-model="e_password" type="password" password placeholder="请输入密码" style="width: 300px; margin-left: 10px"/>
      </div>
      <div style="margin-top: 10px">
        <span>权限</span>
        <Select v-model="e_permission" multiple style="width:300px; margin-left: 10px">
          <Option v-for="item in permissions" :value="item" :key="item">{{ item }}</Option>
        </Select>
      </div>
      <div style="margin-top: 10px">
        <span>部门</span>
        <Select v-model="e_bms" multiple style="width:300px; margin-left: 10px">
          <Option v-for="item in bms" :value="item" :key="item">{{ item }}</Option>
        </Select>
      </div>
    </Modal>

  </div>
</template>

<script>
import {listUserApi, createUserApi, editUserApi, listBmApi} from "../api/query";

export default {
  name: "User",
  data() {
    return {
      show_create: false,
      show_edit: false,
      username: "",
      password: "",
      bms: [],

      permissions: ["学费查询", "助研费查询"],
      e_username: null,
      e_password: null,
      e_permission: null,
      e_bms: null,

      columns: [{
        "title": "用户名",
        "key": "username",
        "width": 150
      }, {
        "title": "上次登录",
        "key": "lastLogin",
        "width": 170
      }, {
        "title": "超级用户",
        "key": "isSuperUser",
        "width": 100
      }, {
        "title": "部门",
        "key": "bms"
      }, {
        "title": "权限",
        "key": "permissions"
      }, {
        title: '操作',
        slot: 'action',
        width: 150,
        align: 'center'
      }],
      users: [],
    }
  },
  async created() {
    this.users = await listUserApi()
    this.bms = await listBmApi()
  },
  methods: {
    async create() {
      if (!this.username) {
        this.$Message.error({content: "用户名不能为空", duration: 5});
        return
      }
      if (!this.password) {
        this.$Message.error({content: "密码不能为空", duration: 5});
        return;
      }
      createUserApi(this.username, this.password);
      this.$Message.success({content: "创建成功", duration: 5});
      this.users = await listUserApi()
    },
    onEdit(username) {
      this.show_edit = true
      this.e_username = username
    },
    async edit() {
      await editUserApi(this.e_username, this.e_password, this.e_bms, this.e_permission)
    }
  },
}
</script>

<style scoped>

</style>