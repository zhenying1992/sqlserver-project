<template>
  <div>
    <div class="line">
      header
    </div>
    <el-row>
      <el-col></el-col>
    </el-row>
    <el-row>
      <el-col :span="5">
        <el-menu
          :default-active="activeIndex"
          class="el-menu-vertical-demo"
          style="min-height: 600px"
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

      </el-col>
      <el-col :span="18" style="height: 600px">
        <div>
          <router-view></router-view>
        </div>
      </el-col>
    </el-row>

    <div>
      footer
    </div>

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
    }
  }
}
</script>

<style scoped>
.line {
  height: 80px;
}
</style>
