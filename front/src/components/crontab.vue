<template>
  <div>
    <div class="div1">
      <el-button type="primary" @click="newTask">新建定时任务</el-button>
    </div>

    <div class="div1">
      <span>已存在任务:</span>
      <el-table :data="cron_task_list" border style="width:100%">
        <el-table-column prop="id" label="编号" width="50px"></el-table-column>
        <el-table-column prop="name" label="任务类型" width="150px"></el-table-column>
        <el-table-column prop="created_time" label="创建时间" width="160px"></el-table-column>
        <el-table-column prop="schedule" sortable label="执行时间" width="120px"></el-table-column>
        <el-table-column prop="params" label="参数"></el-table-column>
        <el-table-column fixed="right" label="操作" width="100px">
          <template slot-scope="scope">
            <el-button type="text" size="small" @click="onDelete(scope.row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </div>

    <el-dialog title="新建定时任务" :visible.sync="adding" style="text-align: left" width="400px">
      <el-form :model="form">
        <el-form-item label="任务类型" label-width="100px">
          <el-select v-model="form.task" placeholder="请选择任务类型" style="width: 220px">
            <el-option :label="item.name" :value="item.name" :key="item.id" v-for="item in task_list"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="执行时间" label-width="100px">
          <el-time-select
            v-model="form.schedule"
            :picker-options="picker_options"
            placeholder="选择时间"
          >
          </el-time-select>
        </el-form-item>
        <el-form-item label="源机器IP" label-width="100px">
          <el-select v-model="form.source_ip" placeholder="请选择机器IP" style="width:220px">
            <el-option :label="item.ip" :value="item.ip" :key="item.id" v-for="item in source_ip_list"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="源机器文件" label-width="100px">
          <el-input v-model="form.source_path" style="width: 220px"></el-input>
        </el-form-item>
        <el-form-item label="目的机器IP" label-width="100px" v-show="show_dest_ip">
          <el-select v-model="form.dest_ip" placeholder="请选择机器IP" style="width:220px">
            <el-option :label="item.ip" :value="item.ip" :key="item.id" v-for="item in dest_ip_list"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="目的机器文件" label-width="100px" v-show="show_dest_path">
          <el-input v-model="form.dest_path" style="width: 220px"></el-input>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="adding = false">取 消</el-button>
        <el-button type="primary" @click="submit">确 定</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
    export default {
        name: "crontab",
        data() {
            return {
                adding: false,
                picker_options: {
                    start: '00:00',
                    step: '00:30',
                    end: '23:00'
                },
                value: '',
                task_list: [],
                cron_task_list: [],
                form: {
                    task: '',
                    schedule: '',
                    source_ip: '',
                    source_path: '',
                    dest_ip: '',
                    dest_path: ''
                },
                source_ip_list: [],
                dest_ip_list: []
            }
        },
        computed: {
            show_dest_ip: function () {
                return this.form.task === '传输文件到远程';
            },
            show_dest_path: function () {
                return this.form.task === '传输文件到远程'
            }
        },
        created() {
            this.getTask();
            this.getCronTask();
            this.getIp()
        },
        methods: {
            getTask() {
                this.$axios({
                    url: '/tasks',
                    method: 'get',
                }).then(resp => {
                    this.task_list = resp.data.data
                })
            },
            getCronTask() {
                this.$axios({
                    url: '/get-cron-task',
                    method: 'get',
                }).then(resp => {
                    this.cron_task_list = resp.data.data
                });
            },
            getIp() {
                this.$axios({
                    url: 'server',
                    method: 'get'
                }).then(resp => {
                    this.source_ip_list = resp.data.data;
                    this.dest_ip_list = resp.data.data;
                })
            },
            onDelete(row) {
                this.$axios({
                    url: 'delete-cron-task',
                    method: 'delete',
                    data: {id: row.id}
                }).then(resp => {
                    this.$message({
                        showClose: true,
                        message: '已成功删除',
                        type: 'success',
                        duration: 3000
                    });
                    this.getCronTask();
                })
            },
            newTask() {
                this.adding = true;
            },
            submit() {
                this.adding = false;
                this.$axios({
                    url: 'create-cron-task',
                    method: 'post',
                    data: this.form
                }).then(resp => {
                    this.$message({
                        showClose: true,
                        message: '新建成功',
                        type: 'success',
                        duration: 3000
                    });
                    this.form = {
                        task: '',
                        schedule: '',
                        source_ip: '',
                        source_path: '',
                        dest_ip: '',
                        dest_path: ''
                    };
                    this.getCronTask();
                })
            }
        }
    }
</script>

<style scoped>
  .div1 {
    text-align: left;
    margin: 10px;
  }
</style>
