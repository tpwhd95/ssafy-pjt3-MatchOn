<template>
  <div class="mx-auto" max-width="720">
    <v-img height="200" src="@/assets/images/logos/logo.png"></v-img>
    <v-card-title>매치 장소와 시간이 확정되었습니다!</v-card-title>

    <v-card-text class="mb-5"
      >대기중인 경기에서 정보를 확인하고 <br />재밌게 스포츠를
      즐기세요!</v-card-text
    >
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
  name: "MatchTrue",
};
</script>

<style>
</style>