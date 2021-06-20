// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import ElementUI from 'element-ui'
import router from './router'
import axios from 'axios'
import 'element-ui/lib/theme-chalk/index.css'

Vue.config.productionTip = false
Vue.use(ElementUI)

axios.defaults.baseURL = '/api';
axios.defaults.withCredentials = true;
axios.interceptors.response.use(
  response => {
    if (response.data.status === 400) {
      ElementUI.Message({
        showClose: true,
        message: '用户未登陆，请重新登陆',
        type: 'error',
        duration: 3000
      });
      window.location.href='/'
    } else {
      return response;
    }
  }, error => {
    ElementUI.Message({
      showClose: true,
      message: '服务端不可用',
      type: 'error',
      duration: 3000
    });
  }
)
Vue.prototype.$axios = axios;

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  components: {App},
  template: '<App/>'
})
