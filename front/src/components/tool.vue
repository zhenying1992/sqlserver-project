<template>
  <div>
    <el-divider content-position="left"><span style="font-size: 20px">服务器</span></el-divider>
    <el-button type="text" @click="server_test = true">服务器连接测试</el-button>
    <el-divider content-position="left"><span style="font-size: 20px">数据库</span></el-divider>
    <el-button type="text" @click="database_test = true">数据库连接测试</el-button>

    <el-dialog title="服务器连接测试" :visible.sync="server_test" width="500px" style="text-align: left">
      <el-form :model="server_form">
        <el-form-item label="服务器IP">
          <el-select v-model="server_form.ip" placeholder="请选择服务器IP">
            <el-option :label="item.ip" :value="item.ip" :key="item.id" v-for="item in ip_list"></el-option>
          </el-select>
        </el-form-item>
      </el-form>

      <div v-show="server_test_start">
        <el-steps :active="server_test_step" align-center>
          <el-step title="初始化" description=""></el-step>
          <el-step title="开始连接" description=""></el-step>
          <el-step title="测试结果" :description="server_test_result" :status="status"></el-step>
        </el-steps>
      </div>
      <div slot="footer" class="dialog-footer">
        <el-button type="primary" @click="onServerTest">开 始</el-button>
      </div>
    </el-dialog>

    <el-dialog title="数据库连接测试" :visible.sync="database_test" width="500px" style="text-align: left">
      <el-form :model="database_form">
        <el-form-item label="机器IP" label-width="100px">
          <el-select v-model="database_form.ip" placeholder="请选择服务器IP">
            <el-option :label="item.ip" :key="item.id" :value="item.ip" v-for="item in ip_list"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="数据库端口" label-width="100px">
          <el-input
            type="number"
            v-model="database_form.port"
            autocomplete="off"
            style="width: 80px"
            min="1"
            max="65535"
            step="1"
          ></el-input>
        </el-form-item>
        <el-form-item label="数据库账号" label-width="100px">
          <el-input v-model="database_form.username" autocomplete="off" style="width: 200px"></el-input>
        </el-form-item>
        <el-form-item label="数据库密码" label-width="100px">
          <el-input v-model="database_form.password" autocomplete="off" style="width: 200px"></el-input>
        </el-form-item>
      </el-form>
      <div v-show="database_test_start">
        <el-steps :active="database_test_step" align-center>
          <el-step title="初始化" description=""></el-step>
          <el-step title="开始连接" description=""></el-step>
          <el-step title="测试结果" :description="database_test_result" :status="status"></el-step>
        </el-steps>
      </div>
      <div slot="footer" class="dialog-footer">
        <el-button type="primary" @click="onDatabaseTest">确 定</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
    export default {
        name: "crontab",
        data() {
            return {
                server_test: false,
                server_test_start: false,
                server_test_step: 0,
                server_test_result: '',
                database_test: false,
                database_test_start: false,
                database_test_step: 0,
                database_test_result: '',
                ip_list: [],
                server_form: {
                    ip: ''
                },
                database_form: {
                    ip: '',
                    port: '',
                    username: '',
                    password: ''
                },
                status: ''
            }
        },
        created() {
            this.getIP()
        },
        methods: {
            getIP() {
                this.$axios({
                    url: 'server',
                    method: 'get'
                }).then(resp => {
                    this.ip_list = resp.data.data;
                })
            },
            onServerTest() {
                this.status = 'wait';
                this.server_test_step = 0;

                this.server_test_start = true;
                this.wait(1000).then(() => {
                    this.server_test_step = 1;
                    this.wait(1000).then(() => {
                        this.server_test_step = 2;
                        this.wait(1000).then(() => {
                            this.$axios({
                                url: 'server-test',
                                method: 'post',
                                data: this.server_form
                            }).then(resp => {
                                if (resp.data.status === true) {
                                    this.server_test_step = 3;
                                    this.server_test_result = resp.data.msg;
                                    this.status = 'success'
                                } else {
                                    this.server_test_step = 3;
                                    this.server_test_result = resp.data.msg;
                                    this.status = 'error'
                                }
                            })
                        })
                    })
                });
            },
            onDatabaseTest() {
                this.status = 'wait';
                this.database_test_step = 0;
                this.database_test_start = true;

                this.wait(1000).then(() => {
                    this.database_test_step = 1;
                    this.wait(1000).then(() => {
                        this.database_test_step = 2;
                        this.wait(1000).then(() => {
                            this.$axios({
                                url: 'database-test',
                                method: 'post',
                                data: this.database_form
                            }).then(resp => {
                                this.database_test_step = 3;
                                this.database_test_result = resp.data.msg;
                                if (resp.data.status === true) {
                                    this.status = 'success'
                                } else {
                                    this.status = 'error'
                                }
                            })
                        })
                    })
                });
            },
            wait(t) {
                return new Promise((resolve) => setTimeout(resolve, t));
            }
        }
    }
</script>

<style scoped>

</style>
