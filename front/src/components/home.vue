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
          style="height: 600px"
          mode="vertical"
          @select="handleSelect"
          background-color="#545c64"
          text-color="#fff"
          active-text-color="#ffd04b">
          <el-menu-item index="1">数据大盘</el-menu-item>
          <el-submenu index="2">
            <template slot="title">任务配置</template>
            <el-menu-item index="2-1">&nbsp定时任务</el-menu-item>
            <el-menu-item index="2-2">&nbsp人工设置</el-menu-item>
            <!--        <el-menu-item index="2-3">选项3</el-menu-item>-->
            <!--        <el-submenu index="2-4">-->
            <!--          <template slot="title">选项4</template>-->
            <!--          <el-menu-item index="2-4-1">选项1</el-menu-item>-->
            <!--          <el-menu-item index="2-4-2">选项2</el-menu-item>-->
            <!--          <el-menu-item index="2-4-3">选项3</el-menu-item>-->
            <!--        </el-submenu>-->
          </el-submenu>
          <el-menu-item index="3">通用工具</el-menu-item>
          <el-menu-item index="4">日志中心</el-menu-item>
        </el-menu>

      </el-col>
      <el-col :span="18">
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
