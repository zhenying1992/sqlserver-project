<template>
  <div class="back">

    <div style="padding-top: 100px; margin:0 auto; width: 30%;">
      <span style="color: black">用户名</span>
      <Input v-model="username" placeholder="请输入用户名" style="width: 200px; margin-left: 10px"></Input>
    </div>

    <div style="margin-top: 10px"></div>

    <div style="margin:0 auto; width: 30%;">
      <span style="margin-left: 13px; color: black">密码</span>
      <Input type="password" v-model="password" placeholder="请输入密码"
             style="width: 200px; margin-left: 10px"></Input>
    </div>
    <div style="margin-top: 20px"></div>
    <div style="margin:0 auto; width: 30%;">
      <Button style="margin-left: 180px" @click="login">登录</Button>
    </div>
  </div>
</template>

<script>
import {Button} from "view-ui-plus";
import {loginApi} from "../api/query";
export default {
  name: "login",
  components: {Button},
  data() {
    return {
      username: "",
      password: ""
    }
  },
  methods: {
    async login() {
      let res = await loginApi(this.username, this.password)
      if (res !== 'failed') {
        window.location.reload()
      }
    },
  }
}
</script>

<style scoped>
.back {
  width: 100%;
  height: 1000px;
  /*height: 100px;*/
  position: relative;
  background-image: url("../../backend.jpeg");
  background-repeat: no-repeat;
  background-size: contain;

}
</style>