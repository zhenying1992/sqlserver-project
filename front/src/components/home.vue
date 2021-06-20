<template>
  <div>
    <el-container>
      <el-header style="background-color: #2f2d2d; height: 60px">
        <div style="text-align: left; float: left">
          <span style="color: white; font-size: 40px;margin-left: 100px">数据库管理中心</span>
        </div>
        <div style="float: right; margin-top: 10px">
          <el-dropdown @command="handleCommand">
            <el-avatar size="large"
                       src="https://cube.elemecdn.com/3/7c/3ea6beec64369c2642b92c6726f1epng.png"></el-avatar>
            <el-dropdown-menu slot="dropdown">
              <el-dropdown-item command="change">修改密码</el-dropdown-item>
              <el-dropdown-item command="logout">退出</el-dropdown-item>
            </el-dropdown-menu>
          </el-dropdown>

        </div>
      </el-header>
      <el-container>
        <el-aside width="150px">
          <el-menu
            :default-active="activeIndex"
            class="el-menu-vertical-demo"
            style="min-height: 700px"
            mode="vertical"
            @select="handleSelect"
            background-color="#545c64"
            text-color="#fff"
            active-text-color="#ffd04b">
            <el-menu-item index="1">
              <i class="el-icon-menu"></i>
              <span slot="title">数据大盘</span>
            </el-menu-item>
            <el-submenu index="2">
              <template slot="title">
                <i class="el-icon-monitor"></i>
                <span slot="title">任务配置</span>
              </template>
              <el-menu-item-group>
                <el-menu-item index="2-1">&nbsp定时任务</el-menu-item>
                <el-menu-item index="2-2">&nbsp人工设置</el-menu-item>
              </el-menu-item-group>
            </el-submenu>
            <el-menu-item index="3">
              <i class="el-icon-setting"></i>
              <span slot="title">通用工具</span>
            </el-menu-item>
            <el-menu-item index="4">
              <i class="el-icon-document"></i>
              <span slot="title">日志中心</span>
            </el-menu-item>
          </el-menu>
        </el-aside>
        <el-container>
          <el-main>
            <router-view></router-view>
          </el-main>
          <el-footer></el-footer>
        </el-container>
      </el-container>
    </el-container>
  </div>
</template>

<script>
export default {
  data() {
    return {
      activeIndex: '1',
      mapping: {
        '1': '/home/dashboard',
        '2-1': '/home/crontab',
        '2-2': '/home/manual',
        '3': '/home/tool',
        '4': '/home/log'
      }
    };
  },
  methods: {
    handleSelect(key, keyPath) {
      this.$router.push(this.mapping[key])
    },
    handleCommand(command) {
      if (command==='logout'){
        this.logout();
      } else if (command==='change') {
        this.changePassword();
      }
    },
    logout(){
      this.$axios({
        url: '/logout',
        method: 'post',
      }).then(resp => {
        if (resp.data.status===true){
          this.$message({
            showClose: true,
            message: '已退出',
            type: 'success',
            duration: 3000
          });
          this.$router.push('/')
        }
      }).catch(resp => {
        this.$message({
          showClose: true,
          message: '服务端不可用',
          type: 'error',
          duration: 3000
        });
      })
    },
    changePassword(){
      this.$router.push('/home/change-password')
    }
  }
}
</script>

<style scoped>
.line {
  height: 80px;
}
</style>
