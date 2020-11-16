<template>
  <div class="h-100" style="margin: 0px">
    <div class="h-100 d-flex justify-center align-center bg-brown">
      <div class="text-center">
        <h1 class="main-text ft-dh mb-5" style="color: white">
          온라인 스포츠 <span class="ft-dh onred bold"> 매칭 </span>서비스
        </h1>
        <img
          src="@/assets/images/logos/full_logo_black.png"
          alt="match-on-logo"
          style="height: 300px"
          class="mb-5"
        />
        <h2 class="main-text" style="color: white">
          본 서비스는 모바일 전용 서비스입니다.
        </h2>
        <h3 style="color: white">
          모바일 기기로 접속 후 스포츠 매치에
          <span class="onred ft-dh bold">온</span> 하세요
        </h3>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "MainSignoutPC",
};
</script>

<style scoped>
.h-100 {
  height: 100%;
}

.bg-brown {
  background-color: rgba(20, 20, 20, 0.918);
}
</style>