<template>
  <div>
    <div class="div1">
      <el-button type="primary" @click="newTask">新建定时任务</el-button>
    </div>

    <div class="div1">
      <span>已存在任务:</span>
      <el-table :data="task_list" border style="width:100%">
        <el-table-column prop="id" label="编号" width="100px"></el-table-column>
        <el-table-column prop="time" label="时间"></el-table-column>
        <el-table-column prop="source_ip" label="源机器"></el-table-column>
        <el-table-column prop="dest_ip" label="目的机器"></el-table-column>
        <el-table-column fixed="right" label="操作" width="100px">
          <template slot-scope="scope">
            <el-button type="text" size="small" @click="onDelete(scope.row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </div>

    <el-dialog title="新建定时任务" :visible.sync="adding" style="text-align: left" width="400px">
      <el-form :model="form">
        <el-form-item label="执行时间" label-width="100px">
          <el-time-select
            v-model="form.time"
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
        <el-form-item label="目的机器IP" label-width="100px">
          <el-select v-model="form.dest_ip" placeholder="请选择机器IP" style="width:220px">
            <el-option :label="item.ip" :value="item.ip" :key="item.id" v-for="item in dest_ip_list"></el-option>
          </el-select>
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
                form: {
                    time: '',
                    source_ip: '',
                    dest_ip: ''
                },
                source_ip_list: [],
                dest_ip_list: []
            }
        },
        beforeMount() {
            this.getTask();
            this.getIp()
        },
        methods: {
            getTask() {
                this.task_list = [
                    {
                        'id': 1,
                        'name': '传输备份文件1',
                        'time': '14:10:10',
                        'source_ip': '192.168.1.1',
                        'dest_ip': '172.1.1.1'
                    },
                    {
                        'id': 2,
                        'name': '传输备份文件2',
                        'time': '14:10:10',
                        'source_ip': '192.168.1.1',
                        'dest_ip': '172.1.1.1'
                    },
                    {
                        'id': 1,
                        'name': '传输备份文件2',
                        'time': '14:10:10',
                        'source_ip': '192.168.1.1',
                        'dest_ip': '172.1.1.1'
                    }
                ]
            },
            getIp() {
                this.source_ip_list = [
                    {'id': 1, 'ip': '192.168.1.1'},
                    {'id': 2, 'ip': '10.10.1.1'}
                ];
                this.dest_ip_list = [
                    {'id': 1, 'ip': '192.168.1.1'},
                    {'id': 2, 'ip': '10.10.1.1'}
                ];
            },
            onDelete() {
                this.getTask();
            },
            newTask() {
                this.adding = true;
            },
            submit() {
                this.adding = false;
                console.log(this.form);
                this.getTask();
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
