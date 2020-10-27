<template>
  <v-container>
    <v-dialog v-model="dialog" max-width="500">
      <v-card>
        <div class="form-structor">
          <div id="loginDiv" class="login">
            <h2 class="form-title" id="login">Login</h2>
            <button class="kakao submit-btn" @click="kakaologin">
              카카오로 로그인
            </button>
          </div>
        </div>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script>
import axios from "axios";
import http from "@/util/http-common";
import { mapState, mapActions } from "vuex";
export default {
  name: "LoginForm",
  props: ["dialog"],
  data() {
    return {};
  },
  methods: {
    kakaologin() {
      const self = this;
      Kakao.Auth.login({
        success: function (res) {
          const token = res.access_token;
          http
            .post("/auth/kakao", {
              access_token: token,
            })
            .then((res) => {
              Kakao.API.request({
                url: "/v2/user/me",
                success: function (res) {
                  var username = res.properties.nickname;
                  var password = res.id;
                  http
                    .post("/login/", {
                      username: username,
                      password: password,
                    })
                    .then((json) => {
                      const data = json.data;
                      self.setToken(data.token);
                      self.setUserProfile(data.user);
                      self.login();
                    })
                    .catch((error) => {
                      console.log(error);
                      window.gapi &&
                        window.gapi.auth2.getAuthInstance().signOut();
                    });
                },
                fail: function (error) {},
              });
            })
            .catch((err) => {
              console.log(err.response);
            });
        },
        fail: function (error) {
          console.log(error);
        },
      });
    },
    login() {
      this.dialog = false;
      this.$emit("closeForm");
    },
    ...mapActions(["setToken", "setUserProfile"]),
  },
  computed: {
    ...mapState(["authorization"]),
  },
  watch: {
    dialog(val) {
      val || this.$emit("closeForm");
    },
  },
};
</script>

<style>
</style>