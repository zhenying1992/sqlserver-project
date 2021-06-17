<template>
  <div style="margin-top: 50px">
    <div style="text-align: left; margin-left: 30px"><h3>磁盘空间</h3></div>
    <div style="text-align:left;">
      <div v-for="item in disk_list" style="display: inline-block; margin-left: 100px">
        <div>
          <el-progress type="circle" :percentage="item.percent" :color="colors"></el-progress>
          <span>{{ item.disk }}</span>
        </div>
      </div>
    </div>

    <el-divider></el-divider>
    <div style="text-align: left; margin-left: 30px"><h3>备份数据</h3></div>

  </div>
</template>

<script>
    export default {
        name: "tool",
        data() {
            return {
                disk_list: [],
                colors: [
                    {color: '#6f7ad3', percentage: 20},
                    {color: '#1989fa', percentage: 40},
                    {color: '#5cb87a', percentage: 60},
                    {color: '#e6a23c', percentage: 80},
                    {color: '#f56c6c', percentage: 100}
                ]
            }
        },
        created() {
            this.getDisk()
        },
        methods: {
            getDisk() {
                this.disk_list = [
                    {
                        'disk': 'C盘',
                        'size': 100,
                        'percent': 30
                    },
                    {
                        'disk': 'D盘',
                        'size': 100,
                        'percent': 70
                    },
                    {
                        'disk': 'E盘',
                        'size': 100,
                        'percent': 10
                    }]
            }
        }
    }
</script>

<style scoped>

</style>
