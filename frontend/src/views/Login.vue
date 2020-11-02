<template>
  <v-row justify="center">
    <v-dialog v-model="dialog" persistent max-width="290">
      <template v-slot:activator="{ on, attrs }">
        <v-btn color="primary" dark v-bind="attrs" v-on="on"> Login </v-btn>
      </template>

      <v-card>
        <v-card-title class="headline"> Login </v-card-title>
        <v-card-actions>
          <v-btn color="green darken-1" text @click="kakaologin">
            카카오 로그인
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
    <v-btn color="primary" dark @click="logout2"> Logout </v-btn>
  </v-row>
</template>

<script>
import axios from "axios";
import http from "@/util/http-common";
import { mapGetters, mapState, mapActions } from "vuex";
export default {
  name: "LoginForm",
  data() {
    return {
      dialog: false,
    };
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
              console.log("asdf");
              Kakao.API.request({
                url: "/v2/user/me",
                success: function (res) {
                  console.log(res);
                  var username = res.properties.nickname;
                  var password = res.id;
                  http
                    .post("/login/", {
                      username: username,
                      password: password,
                    })
                    .then((json) => {
                      console.log(json);
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
    },
    ...mapActions(["logout", "setToken", "setUserProfile"]),
    logout2() {
      if (this.isLoggedIn) {
        this.logout();
        this.$router.push("/");
      }
    },
  },
  computed: {
    ...mapGetters(["isLoggedIn"]),
  },
};
</script>

<style>
</style>