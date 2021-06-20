<template>
  <div>
    <el-form style="width: 300px" label-width="100px">
      <el-form-item label="新密码">
        <el-input v-model="new_password" placeholder="请输入新密码" show-password></el-input>
      </el-form-item>
      <el-form-item label="新密码确认">
        <el-input v-model="confirm_password" placeholder="请输入新密码" show-password></el-input>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="change">提交</el-button>
      </el-form-item>
    </el-form>
  </div>
</template>

<script>
export default {
  data() {
    return {
      new_password: '',
      confirm_password: ''
    }
  },
  methods: {
    change() {
      if (this.new_password !== this.confirm_password) {
          this.$message({
            showClose: true,
            message: '两次输入的密码不一致',
            type: 'error',
            duration: 3000
          });
          return
      }

      this.$axios({
        url: '/change-password',
        method: 'put',
        data: {
          'password': this.new_password,
          'confim_password': this.confim_password
        }
      }).then(resp => {
        if (resp.data.status===true){
          this.$message({
            showClose: true,
            message: '已修改，请重新登陆',
            type: 'success',
            duration: 3000
          });
          this.$router.push('/')
        } else {
          this.$message({
            showClose: true,
            message: resp.data.msg,
            type: 'warning',
            duration: 3000
          });
        }
      })
    }
  }
}
</script>

<style scoped>

</style>
