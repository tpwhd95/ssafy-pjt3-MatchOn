<template>
  <v-container>
    <v-row justify="space-around">
      <v-card width="400">
        <v-card-title class="black--text mt-8">
          <p class="ml-3">
            팀원들을 찾고있습니다.
            <br /><br />
            매칭이 완료되면
            <br />
            푸시알림이발송됩니다.
          </p>
        </v-card-title>

        <v-card-text>
          <div class="font-weight-bold ml-8 mb-2">종목: {{ sportsNameKR }}</div>
          <div class="font-weight-bold ml-8 mb-2">날짜: {{ date1 }}</div>
          <div class="font-weight-bold ml-8 mb-2">
            시간: {{ time[0] }}시 ~ {{ time[1] }}시
          </div>
        </v-card-text>
      </v-card>
    </v-row>

    <v-row justify="space-around">
      <v-col cols="8" class="mt-5">
        <v-progress-linear
          color="deep-purple accent-4"
          indeterminate
          rounded
          height="6"
        ></v-progress-linear>
      </v-col>
    </v-row>

    <v-row>
      <v-col cols="12" class="d-flex justify-center mt-7">
        <v-btn color="primary" @click="main"> 메인으로 돌아가기 </v-btn>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
export default {
  name: "Matching",
  data() {
    return {
      sportsNameKR: this.$route.query.sportsNameKR,
      date1: this.$route.query.date1,
      time: this.$route.query.time,
    };
  },
  methods: {
    main() {
      this.$router.push("/map");
    },
  },
};
</script>

<style>
</style>