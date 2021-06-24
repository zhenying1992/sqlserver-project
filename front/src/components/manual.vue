<template>
  <div>
    <div style="margin-top: 20px; text-align: left;">
      <el-button type="primary" @click="backup">立即备份</el-button>
      <el-button type="primary" @click="transfer">文件传输</el-button>
      <el-button type="primary" @click="deleteFile">删除文件</el-button>
    </div>

    <el-dialog title="文件传输" :visible.sync="adding" style="text-align: left" width="400px">
      <el-form :model="form">
        <el-form-item label="源机器IP" label-width="100px">
          <el-select v-model="form.source_ip" placeholder="请选择机器IP" style="width:220px">
            <el-option :label="item.ip" :value="item.ip" :key="item.id" v-for="item in source_ip_list"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="源机器文件" label-width="100px">
          <el-input v-model="form.source_path" style="width: 220px"></el-input>
        </el-form-item>
        <el-form-item label="目的机器IP" label-width="100px" v-show="show_dest">
          <el-select v-model="form.dest_ip" placeholder="请选择机器IP" style="width:220px">
            <el-option :label="item.ip" :value="item.ip" :key="item.id" v-for="item in dest_ip_list"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="目的机器文件" label-width="100px" v-show="show_dest">
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
        name: "manual",
        data() {
            return {
                adding: false,
                form: {
                    task: '',
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
            show_dest: function () {
                return this.form.task === '传输文件到远程';
            },
        },
        created() {
            this.getIp();
        },
        methods: {
            init() {
                this.form = {
                    task: '',
                    schedule: '',
                    source_ip: '',
                    source_path: '',
                    dest_ip: '',
                    dest_path: ''
                }
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
            backup() {
                this.init();
                this.form.task = '备份数据库到本地';
                this.adding = true;
            },
            transfer() {
                this.init();
                this.form.task = '传输文件到远程';
                this.adding = true;
            },
            deleteFile() {
                this.init();
                this.form.task = '删除文件';
                this.adding = true;
            },
            submit() {
                const loading = this.$loading({
                    lock: true,
                    text: 'Loading',
                    spinner: 'el-icon-loading',
                    background: 'rgba(0, 0, 0, 0.7)'
                });

                this.$axios({
                    url: 'execute',
                    method: 'post',
                    data: this.form
                }).then(resp => {
                    loading.close();
                    if (resp.data.status === true) {
                        this.$message({
                            showClose: true,
                            message: '已成功删除',
                            type: 'success',
                            duration: 3000
                        });
                    } else {
                        loading.close();
                        this.$message({
                            showClose: true,
                            message: '执行失败',
                            type: 'failed',
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
