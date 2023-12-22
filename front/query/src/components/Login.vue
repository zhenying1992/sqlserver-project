<template>
  <div class="back">
    <div style="height: 100px"></div>
    <div style="width:30%; margin: auto; background: rgba(255,255,255,0.3); text-align: center;border: 1px; border-radius: 20px;">
      <div style="font-size: 30px; text-align: center; padding-top: 10px">查询系统</div>
      <div style="margin-top: 10px">
        <span style="color: black;font-size: 20px">用户名</span>
        <Input v-model="username" placeholder="请输入用户名" style="width: 200px; margin-left: 10px;"
               size="large"></Input>
      </div>

      <div style="margin-top: 10px"></div>

      <div>
        <span style="margin-left: 13px; color: black; font-size: 20px">密码</span>
        <Input type="password" v-model="password" placeholder="请输入密码"
               style="width: 200px; margin-left: 16px" size="large"></Input>
      </div>
      <div style="margin-top: 20px"></div>
      <div>
        <Button style="margin-left: 180px" @click="login" size="large">登录</Button>
      </div>
      <div style="height: 20px"></div>
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
  background-size: 100%;
  background-position: unset;

}
</style>