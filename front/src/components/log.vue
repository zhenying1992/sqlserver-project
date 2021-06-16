<template>

  <div style="margin-top: 20px">
    <div class="block">
      <span class="demonstration">请选择时间&nbsp&nbsp&nbsp</span>
      <el-date-picker
        v-model="pick_date"
        type="daterange"
        align="right"
        unlink-panels
        range-separator="至"
        start-placeholder="开始日期"
        end-placeholder="结束日期"
        value-format="timestamp"
        @change="OnDate"
        :picker-options="pickerOptions">
      </el-date-picker>
    </div>
    <div class="block" style="margin-top: 20px">
      <el-timeline>
        <el-timeline-item v-for="item in activities" :timestamp="item.timestamp" placement="top"
                          style="text-align: left" :key="item.id">
          <el-card>
            <h4>{{item.title}}</h4>
            <span>{{item.content}}</span>
          </el-card>
        </el-timeline-item>
      </el-timeline>
    </div>
  </div>
</template>

<script>
    export default {
        data() {
            return {
                pick_date: '',
                pickerOptions: {
                    disabledDate(time) {
                        return time.getTime() > Date.now();
                    }
                },
                activities: []
            };
        },
        methods: {
            OnDate() {
              console.log(this.pick_date)
              this.activities= [
                {
                  id: 1,
                  content: '从192.168.1.1同步数据到192.168.1.100成功',
                  timestamp: '2018-04-12 20:46',
                  title: '备份任务同步'
                },
                {
                  id: 1,
                  content: '从192.168.1.1同步数据到192.168.1.100成功',
                  timestamp: '2018-04-03 20:46',
                  title: '备份任务同步'
                }, {
                  id: 1,
                  content: '从192.168.1.1同步数据到192.168.1.100成功',
                  timestamp: '2018-04-03 20:46',
                  title: '备份任务同步'
                },
                {
                  id: 1,
                  title: '备份任务同步',
                  content: '从192.168.1.1同步数据到192.168.1.100成功',
                  timestamp: '2018-04-03 20:46'
                }]
            }
        }
    };
</script>

<style scoped>

</style>
