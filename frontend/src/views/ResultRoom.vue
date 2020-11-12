<template>
  <v-card class="mx-auto" max-width="720">
    <h1>경기결과 입력</h1>
    <p>경기 번호: {{ match_id }}</p>
    <p>종목: {{ sports }}</p>
    <p>날짜: {{ date }}</p>
    <p>시간: {{ time | ChangeTime }}시</p>
    <v-btn @click="inputResultWin">승리</v-btn>
    <v-btn @click="inputResultLose">패배</v-btn>
  </v-card>
</template>

<script>
import http from "@/util/http-common";
import { mapState } from "vuex";

export default {
  name: "ResultRoom",
  components: {},
  data() {
    return {
      match_id: this.$route.params.match_id,
      sports: this.$route.params.sports,
      date: this.$route.params.date,
      time: this.$route.params.time,
    };
  },
  computed: {
    ...mapState(["token"]),
  },
  methods: {
    inputResultWin() {
      http
        .post(
          "/match/result/",
          {
            match_pk: this.match_id,
            result: "true",
          },
          {
            headers: {
              Authorization: "JWT " + this.token,
            },
          }
        )
        .then((res) => {
          console.log(res);
          if (res.data.result == "ready") {
            console.log("ready");
            this.$router.push("/resultready");
          } else if (res.data.result == "error") {
            console.log("error");
            this.$router.push("/resulterror");
          } else if (res.data.result == "false") {
            console.log("false");
            this.$router.push("/resultfalse");
          } else if (res.data.result == "true") {
            console.log("true");
            this.$router.push("/resulttrue");
          }
        })
        .catch((err) => {
          console.log(err);
        });
    },
    inputResultLose() {
      http
        .post(
          "/match/result/",
          {
            match_pk: this.match_id,
            result: "false",
          },
          {
            headers: {
              Authorization: "JWT " + this.token,
            },
          }
        )
        .then((res) => {
          console.log(res);
          if (res.data.result == "ready") {
            console.log("ready");
            this.$router.push("/resultready");
          } else if (res.data.result == "error") {
            console.log("error");
            this.$router.push("/resulterror");
          } else if (res.data.result == "false") {
            console.log("false");
            this.$router.push("/resultfalse");
          } else if (res.data.result == "true") {
            console.log("true");
            this.$router.push("/resulttrue");
          }
        })
        .catch((err) => {
          console.log(err);
        });
    },
  },
  filters: {
    ChangeTime(value) {
      return value.split(":")[0];
    },
  },
};
</script>

<style>
</style>