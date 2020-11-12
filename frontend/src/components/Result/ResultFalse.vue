<template>
  <v-card class="mx-auto" max-width="720">
    <h1>양팀의 게임 결과가 일치하지 않습니다. 결과를 다시 입력해주세요.</h1>
    <v-btn @click="$router.go(-1)">이전 화면으로</v-btn>
  </v-card>
</template>

<script>
export default {
  name: "ResultFalse",
};
</script>

<style>
</style>