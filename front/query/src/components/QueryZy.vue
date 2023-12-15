<template>
  <div>
    <Row>
      <Col span="7">
        <span style="margin-left: 30px">学号</span>
        <Input v-model="xh" placeholder="请输入学号" style="width: 200px"/>
      </Col>
      <Col span="7">
        <span>部门编号</span>
        <Input v-model="bmbh" placeholder="请输入部门编号" style="width: 200px"/>
      </Col>
      <Col span="7">
        <span>项目编号</span>
        <Input v-model="xmbh" placeholder="请输入项目编号" style="width: 200px"/>
      </Col>
    </Row>

    <Row style="margin-top: 10px">
      <Col span="7">
        <span>发放项目</span>
        <Select v-model="ffxm" style="width:200px">
          <Option v-for="item in xms" :value="item" :key="item">{{ item }}</Option>
        </Select>
      </Col>
      <Col span="10">
        <span>发放年月</span>
        <DatePicker type="month" format="yyyy/MM" placeholder="选择开始年月" v-model="ffnyStart" style="width: 200px"/>
        <span style="margin-left: 15px">至</span>
        <DatePicker type="month" format="yyyy/MM" placeholder="选择结束年月" v-model="ffnyEnd" style="width: 200px"/>
      </Col>
      <Col>
        <Button type="primary" @click="search">查询</Button>
        <Button type="primary" @click="download" style="margin-left: 3px">下载</Button>
      </Col>
    </Row>

    <div style="margin-top: 20px">
      <Table :columns="columns" :data="pagination.data"></Table>
    </div>

    <div style="float: right; margin-top: 10px">
      <Page
          :value="pagination.current"
          :total="pagination.total"
          :page-size="pagination.size"
          show-sizer
          @on-change="click"
          @on-prev=""
          @on-next=""
          @on-page-size-change="sizeChange"
      />
    </div>


  </div>
</template>

<script>
import {Input, Row} from "view-ui-plus";
import {getZyColumnApi, getZyDataApi, listBmApi, listXmApi} from "../api/query";

export default {
  name: "Query",
  components: {Row, Input},
  data() {
    return {
      xh: "",
      bmbh: '',
      xmbh: '',
      ffnyStart: '',
      ffnyEnd: '',
      ffxm: '',
      isDownload: false,

      xms: [],

      columns: [],

      pagination: {
        current: 1,
        total: 0,
        pageSize: 10,
        data: []
      }
    }
  },
  async created() {
    this.bms = await listBmApi();
    this.xms = await listXmApi();
    this.columns = await getZyColumnApi();
  },
  methods: {
    change(value) {
      this.showModule = value
    },
    async query() {
      let ffnyStart = undefined;
      if (this.ffnyStart) {
        let month = this.ffnyStart.getMonth() + 1;
        month = month.toString().padStart(2, '0')
        ffnyStart = this.ffnyStart.getFullYear() + "-" + month;
      }

      let ffnyEnd = undefined;
      if (this.ffnyEnd) {
        let month = this.ffnyEnd.getMonth() + 1;
        month = month.toString().padStart(2, '0')
        ffnyEnd = this.ffnyEnd.getFullYear() + "-" + month;
      }

      this.pagination = await getZyDataApi(
          this.xh, this.bmbh, this.xmbh, ffnyStart, ffnyEnd, this.ffxm, this.pagination, this.isDownload
      )
    },
    async click(page) {
      this.pagination.current = page
      await this.query()
    },
    async sizeChange(size) {
      this.pagination.pageSize = size;
      this.pagination.current = 1;
      await this.query()
    },
    async search() {
      this.isDownload = false;
      await this.query();
    },
    async download() {
      this.isDownload = true;
      await this.query();
    }
  }
}
</script>

<style scoped>
span {
  margin-right: 10px
}

</style>