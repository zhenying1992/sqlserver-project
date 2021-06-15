<template>
  <div class="login">
    <div style="margin-bottom: 100px; font-size: 50px;width:450px">财务数据库管理系统</div>
    <el-form :model="form" label-width="100px">
      <el-form-item prop="username" label="账号">
        <el-input v-model="form.username"></el-input>
      </el-form-item>

      <el-form-item prop="password" label="密码">
        <el-input v-model="form.password"></el-input>
      </el-form-item>

      <el-form-item>
        <el-button type="primary" @click="submit">提交</el-button>
        <el-button @click="reset">重置</el-button>
      </el-form-item>
    </el-form>
  </div>
</template>

<script>
    export default {
        data() {
            return {
                form: {
                    username: "",
                    password: ""
                }
            }
        },
        methods: {
            submit() {
                this.$router.push('/home/dashboard')
            },
            reset() {
                this.form.username = "";
                this.form.password = "";
            }
        }
    }
</script>

<style scoped>
  .login {
    position: absolute;
    width: 400px;
    height: 150px;
    margin: auto;
    margin-top: 300px;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
  }
</style>
