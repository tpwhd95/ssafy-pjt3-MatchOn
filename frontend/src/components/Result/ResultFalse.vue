<template>
  <div class="mx-auto d-flex" max-width="720" style="height: 100%">
    <div class="align-self-center">
      <v-card-title>양팀의 게임 결과가 일치하지 않습니다.</v-card-title>

      <v-card-text class="mb-5"> 결과를 다시 입력해주세요. </v-card-text>
      <div class="d-flex justify-center">
        <v-btn
          color="error"
          class="mt-10 mb-15"
          @click="$router.push('/schedule')"
          >내 일정으로</v-btn
        >
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "ResultFalse",
};
</script>

<style>
</style>