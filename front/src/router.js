import Vue from 'vue'
import Router from 'vue-router'
import Login from '@/components/login'
import Dashboard from '@/components/dashboard'
import Home from '@/components/home'
import Crontab from '@/components/crontab'
import Manual from '@/components/manual'
import Log from '@/components/log'
import Tool from '@/components/tool'
import ChangePassword from '@/components/change-password'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      component: Login
    },
    {
      path: '/login',
      component: Login
    },
    {
      path: '/home',
      component: Home,
      children: [
        {
          path: 'dashboard',
          component: Dashboard
        },
        {
          path: 'tool',
          component: Tool
        },
        {
          path: 'log',
          component: Log
        },
        {
          path: 'manual',
          component: Manual
        },
        {
          path: 'crontab',
          component: Crontab
        },
        {
          path: 'change-password',
          component: ChangePassword
        }
      ]
    }
  ]
})
