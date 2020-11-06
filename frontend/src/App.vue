<template>
  <v-app>
    <v-app-bar app color="primary" dark>
      <div class="d-flex align-center">
        <h1 @click="$router.push('/')" style="cursor: pointer">Match On</h1>
      </div>

      <v-spacer></v-spacer>

      <v-dialog v-if="!this.isLoggedIn" v-model="dialog" max-width="500">
        <template v-slot:activator="{ on, attrs }">
          <v-btn color="primary" dark v-bind="attrs" v-on="on"> Login </v-btn>
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

      <p
        v-if="this.isLoggedIn"
        style="margin: 0px 16px 0px 0px; cursor: pointer"
        @click="profile"
      >
        마이페이지
      </p>
      <v-btn v-if="this.isLoggedIn" color="primary" dark @click="logout2">
        Logout
      </v-btn>
    </v-app-bar>

    <v-main>
      <br />
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
    profile() {
      this.$router.push("/profile");
    },
  },
  computed: {
    ...mapGetters(["isLoggedIn"]),
  },
};
</script>
