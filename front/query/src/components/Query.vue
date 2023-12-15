<template>
  <div>
    <Row>
      <Col span="7">
        <span style="margin-left: 30px">学号</span>
        <Input v-model="xh" placeholder="请输入学号" style="width: 200px"/>
      </Col>
      <Col span="7">
        <span style="margin-left: 30px">姓名</span>
        <Input v-model="xm" placeholder="请输入姓名" style="width: 200px"/>
      </Col>
      <Col span="10">
        <span>部门名称</span>
        <Select v-model="bm" style="width: 200px">
          <Option v-for="option in bms" :value="option" :key="option">{{ option }}</Option>
        </Select>
      </Col>
    </Row>

    <Row style="margin-top: 10px">
      <Col span="7">
        <span>入学年度</span>
        <DatePicker type="year" format="yyyy" placeholder="选择入学年度" v-model="rxnd" style="width: 200px"/>
      </Col>
      <Col span="7">
        <span>收费年度</span>
        <DatePicker type="year" format="yyyy" placeholder="选择缴费年度" v-model="sfnd" style="width: 200px"/>
      </Col>
      <Col span="5">
        <span>是否欠费</span>
        <Checkbox v-model="sfqf">&nbsp</Checkbox>
      </Col>
      <Col>
        <Button type="primary" @click="search">查询</Button>
        <Button type="primary" @click="download" style="margin-left: 5px">下载</Button>
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
          @on-change="query"
          @on-prev="query"
          @on-next="query"
          @on-page-size-change="query"
      />
    </div>

  </div>
</template>

<script>
import {Input} from "view-ui-plus";
import {getDataApi, listBmApi, getColumnApi} from "../api/query";

export default {
  name: "QueryZy",
  components: {Input},
  data() {
    return {
      xh: undefined,
      xm: undefined,
      bm: undefined,
      bms: [],
      rxnd: undefined,
      sfnd: undefined,
      sfqf: undefined,
      columns: [],
      isDownload: Boolean,

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
    this.columns = await getColumnApi();
  },
  methods: {
    change(value) {
      this.showModule = value
    },
    async query() {
      let rxnd = undefined;
      if (this.rxnd) {
        rxnd = this.rxnd.getFullYear();
      }

      let sfnd = undefined;
      if (this.sfnd) {
        sfnd = this.sfnd.getFullYear();
      }

      this.pagination = await getDataApi(
          this.xh, this.xm, this.bm, rxnd, sfnd, this.sfqf, this.pagination, this.isDownload
      )
    },
    async search() {
      this.isDownload = false;
      await this.query();
    },
    async download() {
      this.isDownload = true;
      await this.query()
    }
  }
}
</script>

<style scoped>
span {
  margin-right: 10px
}

</style>