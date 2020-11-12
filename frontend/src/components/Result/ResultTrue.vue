<template>
  <v-card class="mx-auto" max-width="720">
    <h1>승패 입력에 대한 처리가 완료되었습니다. 결과를 확인해주세요.</h1>
    <v-btn @click="$router.push('/profile')">마이페이지로</v-btn>
  </v-card>
</template>

<script>
export default {
  name: "ResultTrue",
};
</script>

<style>
</style>