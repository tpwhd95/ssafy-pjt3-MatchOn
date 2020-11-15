import Vue from 'vue'
import VueRouter from 'vue-router'

import Home from '../views/Home.vue'
import About from '../views/About.vue'
import Schedule from '../views/Schedule.vue'
import Match from '../views/Match.vue'
import Matching from '../views/Matching.vue'
import HowToUse from '../views/HowToUse.vue'
import MatchRoom from '../views/MatchRoom.vue'
import ResultRoom from '../views/ResultRoom.vue'
import ResultReady from '../components/Result/ResultReady.vue'
import ResultFalse from '../components/Result/ResultFalse.vue'
import ResultTrue from '../components/Result/ResultTrue.vue'
import MatchTrue from '../components/Result/MatchTrue.vue'
import Login from "../views/Login.vue";
import Chat from "../views/Chat.vue";
import Report from "../views/Report.vue";
import ReportDetail from "../views/ReportDetail.vue";

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/about/:sports',
    name: 'About',
    component: About
  },
  {
    path: '/schedule',
    name: 'Schedule',
    component: Schedule
  },
  {
    path: '/match',
    name: 'Match',
    component: Match
  },
  {
    path: '/matching',
    name: 'Matching',
    component: Matching
  },
  {
    path: '/howtouse',
    name: 'HowToUse',
    component: HowToUse
  },
  {
    path: '/matchroom/:match_id',
    name: 'MatchRoom',
    component: MatchRoom
  },
  {
    path: '/resultroom/:match_id',
    name: 'ResultRoom',
    component: ResultRoom
  },
  {
    path: '/resultready',
    name: 'ResultReady',
    component: ResultReady
  },
  {
    path: '/resultfalse',
    name: 'ResultFalse',
    component: ResultFalse
  },
  {
    path: '/resulttrue',
    name: 'ResultTrue',
    component: ResultTrue
  },
  {
    path: '/matchtrue',
    name: 'MatchTrue',
    component: MatchTrue
  },
  {
    path: "/login",
    name: "Login",
    component: Login
  },
  {
    path: '/chat',
    name: 'Chat',
    component: Chat,
    props: true,
    beforeEnter: (to, from, next) => {
      if (to.params.name) {
        next();
      } else {
        next({ name: 'Login' })
      }
    }
  },
  {
    path: "/report",
    name: "Report",
    component: Report
  },
  {
    path: "/report/:sports_pk",
    name: "ReportDetail",
    component: ReportDetail
  },
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router
