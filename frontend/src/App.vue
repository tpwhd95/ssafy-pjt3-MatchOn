<template>
  <v-app>
    <v-app-bar app color="grey darken-3" dark>
      <v-app-bar-nav-icon @click.stop="drawer = !drawer"></v-app-bar-nav-icon>
      <div>
        <h1 @click="$router.push('/')" style="cursor: pointer">Match On</h1>
      </div>

      <v-spacer></v-spacer>

      <v-dialog v-if="!this.isLoggedIn" v-model="dialog" max-width="500">
        <template v-slot:activator="{ on, attrs }">
          <v-btn color="teal" dark v-bind="attrs" v-on="on"> Login </v-btn>
        </template>
        <v-card style="padding: 20px">
          <v-card-title
            class="headline d-flex justify-center"
            style="padding: 0px 0px 20px 0px"
          >
            Login
          </v-card-title>
          <v-card-actions>
            <v-img
              src="@/assets/kakao_login_large_wide.png"
              @click="kakaologin"
              style="cursor: pointer"
            >
            </v-img>
          </v-card-actions>
        </v-card>
      </v-dialog>

      <v-btn v-if="this.isLoggedIn" color="teal" dark @click="logout2">
        Logout
      </v-btn>
    </v-app-bar>

    <v-navigation-drawer v-model="drawer" absolute left temporary dark>
      <v-list nav dense>
        <v-list-item-group v-model="group">
          <v-list-item style="margin: 12px 3px">
            <v-list-item-title @click="$router.push('/')">
              <h1 class="display-1 font-weight-bold">
                Match On
              </h1></v-list-item-title
            >
          </v-list-item>

          <v-list-item v-if="this.isLoggedIn" style="margin: 6px 3px">
            <v-list-item-title @click="$router.push('/profile')">
              <span class="text-h6 font-weight-bold">
                마이페이지
              </span></v-list-item-title
            >
          </v-list-item>

          <v-list-item style="margin: 6px 3px">
            <v-list-item-title @click="$router.push('/howtouse')">
              <span class="text-h6 font-weight-bold">
                이용방법
              </span></v-list-item-title
            >
          </v-list-item>
        </v-list-item-group>
      </v-list>
    </v-navigation-drawer>

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
      drawer: false,
      group: null,
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
              console.log("Login Success");
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
  watch: {
    group() {
      this.drawer = false;
    },
  },
};
</script>
