<template>
  <div>
    <div>
      <el-time-select
        v-model="value"
        :picker-options="{
    start: '08:30',
    step: '00:15',
    end: '18:30'
  }"
        placeholder="选择时间">
      </el-time-select>
    </div>
  </div>
</template>

<script>
    export default {
        name: "crontab",
        data() {
            return {
                picker_options: {
                    start: '00:00',
                    step: '00:30',
                    end: '23:00'
                }
            }
        }
    }
</script>

<style scoped>

</style>
