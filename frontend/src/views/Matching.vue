<template>
  <v-container>
    <v-row justify="space-around">
      <v-card width="400">
        <!-- <v-img height="100%" src="@/assets/son.jpg"> -->
        <v-card-title class="black--text mt-8">
          <p class="ml-3">
            Wonbin님 팀원들을 찾고있습니다. <br /><br />매칭이 완료되면
            <br />푸시알림이 발송됩니다.
          </p>
        </v-card-title>
        <!-- </v-img> -->

        <v-card-text>
          <div class="font-weight-bold ml-8 mb-2">종목: 풋살</div>
          <div class="font-weight-bold ml-8 mb-2">날짜: 2020년 11월 5일</div>
          <div class="font-weight-bold ml-8 mb-2">
            시간: 오전 6시 ~ 오후 10시
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
        <v-btn color="primary" @click="main()"> 메인으로 돌아가기 </v-btn>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
export default {
  name: "matching",
  data() {
    return {};
  },
  methods: {
    main() {
      // this.$router.push("/");
      this.$router.push("/map");
    },
  },
};
</script>

<style>
</style>