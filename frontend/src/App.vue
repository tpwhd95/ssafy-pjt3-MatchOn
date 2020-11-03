<template>
  <v-app>
    <v-app-bar app color="primary" dark>
      <div class="d-flex align-center">
        <v-img
          alt="Vuetify Logo"
          class="shrink mr-2"
          contain
          src="https://cdn.vuetifyjs.com/images/logos/vuetify-logo-dark.png"
          transition="scale-transition"
          width="40"
          @click="$router.push('/')"
        />
      </div>

      <v-spacer></v-spacer>

      <v-dialog
        v-if="!this.isLoggedIn"
        v-model="dialog"
        persistent
        max-width="290"
      >
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
      <v-text-field
        v-if="this.isLoggedIn"
        v-model="userProfile.username"
        width="50"
        readonly
        dense
      />
      <v-btn v-if="this.isLoggedIn" color="primary" dark @click="logout2">
        Logout
      </v-btn>
    </v-app-bar>

    <v-main>
      <router-view></router-view>
    </v-main>
  </v-app>
</template>

<script>
import axios from "axios";
import http from "@/util/http-common";
import { mapGetters, mapState, mapActions } from "vuex";

export default {
  name: "app",
  data() {
    return {
      dialog: false,
      userProfile: sessionStorage.getItem("userProfile")
        ? JSON.parse(sessionStorage.getItem("userProfile"))
        : [],
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
                  username = username.replace(/(\s*)/g, "");
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
