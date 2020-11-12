<template>
  <v-card class="mx-auto" max-width="720">
    <h1>경기결과 입력</h1>
    <p>경기 번호: {{ match_id }}</p>
    <p>종목: {{ sports }}</p>
    <p>날짜: {{ date }}</p>
    <p>시간: {{ time }}</p>
    <v-btn @click="inputResultWin">승리</v-btn>
    <v-btn @click="inputResultLose">패배</v-btn>
  </v-card>
</template>

<script>
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
        })
        .catch((err) => {
          console.log(err);
        });
    },
  },
};
</script>

<style>
</style>