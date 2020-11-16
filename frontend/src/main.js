import Vue from 'vue'
import Vuex from 'vuex'
import App from './App.vue'
import './registerServiceWorker'
import router from './router'
import store from './store'
import vuetify from './plugins/vuetify';
import VueChatScroll from 'vue-chat-scroll';
import Directives from './plugins/directives';
// Global Font Css
import "@/assets/font/font.css";

Vue.config.productionTip = false
Vue.use(Vuex)
Vue.use(Directives);
Vue.use(VueChatScroll);



new Vue({
  created() {
    Kakao.init('e4263be1d8a351bad145638cb6ade0bd')
  },
  router,
  store,
  vuetify,
  // socket,
  render: h => h(App)
}).$mount('#app')