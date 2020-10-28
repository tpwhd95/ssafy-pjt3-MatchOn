import Vue from 'vue'
import Vuex from 'vuex'
import App from './App.vue'
import './registerServiceWorker'
import router from './router'
import store from './store'
import vuetify from './plugins/vuetify';

Vue.config.productionTip = false
Vue.use(Vuex)

new Vue({
  created() {
    Kakao.init('e4263be1d8a351bad145638cb6ade0bd')
  },
  router,
  store,
  vuetify,
  render: h => h(App)
}).$mount('#app')
