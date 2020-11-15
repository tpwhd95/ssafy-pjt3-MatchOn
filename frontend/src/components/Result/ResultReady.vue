<template>
  <div class="mx-auto d-flex" max-width="720" style="height: 100%">
    <div class="align-self-center">
      <v-card-title>다른 팀의 결과 입력을 기다리고 있습니다.</v-card-title>

      <v-card-text class="mb-5"> 잠시만 기다려주세요. </v-card-text>
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
  name: "ResultReady",
};
</script>

<style>
</style>