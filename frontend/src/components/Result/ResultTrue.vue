<template>
  <div class="mx-auto" max-width="720">
    <v-img height="200" src="@/assets/images/logos/logo.png"></v-img>

    <v-card-title>승패 입력에 대한 처리가 완료되었습니다!</v-card-title>

    <v-card-text class="mb-5">
      완료된 경기에서 결과를 확인해주세요.
    </v-card-text>
    <div class="d-flex justify-center">
      <v-btn
        color="error"
        class="mt-10 mb-15"
        @click="$router.push('/schedule')"
        >내 일정으로</v-btn
      >
    </div>
  </div>
</template>

<script>
export default {
  name: "ResultTrue",
};
</script>

<style>
</style>