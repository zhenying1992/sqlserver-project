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
        value-format="yyyy-MM-dd HH:mm:ss"
        @change="OnDate"
        :picker-options="pickerOptions">
      </el-date-picker>
    </div>
    <div class="block" style="margin-top: 20px">
      <el-timeline>
        <el-timeline-item v-for="item in activities" :timestamp="item.created_time" placement="top"
                          style="text-align: left" :key="item.id">
          <el-card>
            <h4>{{item.name}}</h4>
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
              this.$axios({
                url: '/log',
                method: 'post',
                data: this.pick_date
              }).then(resp =>{
                this.activities=resp.data.data;
              })
            }
        }
    };
</script>

<style scoped>

</style>
