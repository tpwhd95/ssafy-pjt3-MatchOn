import Vue from 'vue'
import VueRouter from 'vue-router'
import Home from '../views/Home.vue'
import Map from '../views/Map.vue'
import MapTest from '../views/Maptest.vue'
import MapTest2 from '../views/Maptest2.vue'
import ChatRoom from '../views/ChatRoom.vue'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/about',
    name: 'About',
    component: () => import(/* webpackChunkName: "about" */ '../views/About.vue')
  },
  {
    path: '/map',
    name: 'Map',
    component: Map

  },
  {
    path: '/maptest',
    name: 'MapTest',
    component: MapTest
  },
  {
    path: '/maptest2',
    name: 'MapTest2',
    component: MapTest2
  },
  {
    path: '/chatroom/:username',
    name: 'ChatRoom',
    component: ChatRoom
  },
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router
