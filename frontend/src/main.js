import Vue from 'vue'
import Vuex from 'vuex'
import App from './App.vue'
import './registerServiceWorker'
import router from './router'
import store from './store'
import vuetify from './plugins/vuetify';
import socket from './plugins/socketPlugin';
import Directives from './plugins/directives';

Vue.config.productionTip = false
Vue.use(Vuex)
Vue.use(Directives);

new Vue({
  created() {
    Kakao.init('e4263be1d8a351bad145638cb6ade0bd')
  },
  router,
  store,
  vuetify,
  socket,
  render: h => h(App)
}).$mount('#app')