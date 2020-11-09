import Vue from "vue";
import Vuex from "vuex";
import http from "@/util/http-common";

Vue.use(Vuex);

const debug = process.env.NODE_ENV !== 'production';

export default new Vuex.Store({
  state: {
    token: sessionStorage.getItem('token'),
    userProfile: sessionStorage.getItem("userProfile") ? JSON.parse(sessionStorage.getItem("userProfile")) : [],
  },
  getters: {
    isLoggedIn(state) {
      if (state.userProfile != null && state.userProfile && state.userProfile != "" && state.userProfile != "null") {
        return true
      }
      return false
    },
  },
  mutations: {
    setToken(state, payload) {
      state.token = payload;
      sessionStorage.setItem("token", payload)
    },
    logout(state) {
      state.token = ''
      state.userProfile = []
      sessionStorage.clear()
    },
    setUserProfile(state, payload) {
      state.userProfile = payload
      sessionStorage.setItem("userProfile", JSON.stringify(payload))
    },
  },
  actions: {
    setToken(context, payload) {
      context.commit("setToken", payload);
    },
    logout(context) {
      context.commit("logout");
    },
    setUserProfile(context, payload) {
      context.commit("setUserProfile", payload)
    },
  },
  strict: debug,
});