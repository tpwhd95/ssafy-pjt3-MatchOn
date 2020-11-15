<template>
  <v-card class="mx-auto" max-width="720">
    <h1>매치 장소와 시간이 확정되었습니다!</h1>
    <h2>대기중인 매치에서 정보를 확인하고 재밌게 스포츠를 즐기세요!</h2>
    <v-btn @click="$router.push('/profile')">마이페이지로</v-btn>
  </v-card>
</template>

<script>
export default {
  name: "MatchTrue",
};
</script>

<style>
</style>