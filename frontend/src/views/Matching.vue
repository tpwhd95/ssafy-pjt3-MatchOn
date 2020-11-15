<template>
  <v-container class="h-100 mt-15">
    <div class="text-center">
      <img
        src="@/assets/images/logos/logo.png"
        alt="awesome-logo-image"
        style="height: 150px"
      />
    </div>
    <div class="text-center">
      <h2 class="bold">매칭이 성공적으로 등록되었습니다!</h2>
    </div>
    <div class="my-3">
      <p class="font-weight-bold text-center mb-0">
        {{ date1 | ChangeDate }} {{ time[0] | ChangeTime }}시부터
        {{ time[1] | ChangeTime }}시까지
      </p>
      <p class="font-weight-bold text-center mb-0">
        {{ sportsNameKR }} 매치가 가능한 상대들을 찾습니다.
      </p>
    </div>

    <div class="text-center">
      <h3 class="bold">매칭이 완료되면 푸쉬알림으로 알려드립니다.</h3>
    </div>

    <div class="my-5">
      <v-progress-linear
        color="red accent-4"
        indeterminate
        rounded
        height="6"
      ></v-progress-linear>
      <p class="text-center" style="font-size: 12px">
        잠시후 메인페이지로 이동합니다.
      </p>
    </div>
    <div class="text-center">
      <v-btn color="error" @click="main"> 메인으로 돌아가기 </v-btn>
    </div>
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
      this.$router.push("/");
    },
    test() {
      console.log("Hey Listen!");
    },
  },
  mounted() {
    setTimeout(this.main, 5000);
  },
  filters: {
    ChangeDate(value) {
      var svalue = value.split("-");
      var newDate = svalue[0] + "년 " + svalue[1] + "월 " + svalue[2] + "일";
      return newDate;
    },
    ChangeTime(value) {
      if (value < 12) {
        return "오전" + value;
      } else if (value == 12) {
        return "오후 12";
      } else {
        return "오후" + (value - 12);
      }
    },
  },
};
</script>

<style>
</style>