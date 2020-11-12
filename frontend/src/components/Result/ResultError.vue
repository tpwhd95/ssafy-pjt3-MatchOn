<template>
  <v-card class="mx-auto" max-width="720">
    <h1>이미 결과를 투표하셨습니다.</h1>
    <v-btn @click="$router.push('/')">홈으로</v-btn>
  </v-card>
</template>

<script>
export default {
  name: "ResultError",
};
</script>

<style>
</style>