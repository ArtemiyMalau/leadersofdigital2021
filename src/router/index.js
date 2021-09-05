import Vue from 'vue'
import VueRouter from 'vue-router'

import searchMainPage from '../components/searchMainPage';
import personalAreaPage from '../components/personalAreaPage';

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    component: searchMainPage
  },
  {
    path: '/personalArea',
    component: personalAreaPage
  }
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router
