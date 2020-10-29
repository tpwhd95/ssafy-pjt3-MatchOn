<template>
  <div class="maptest2">
    <div id="map" style="width: 100%; height: 600px"></div>
  </div>
</template>

<script>
export default {
  mounted() {
    window.kakao && window.kakao.maps ? this.initMap() : this.addScript();
  },
  data: () => {
    return {
      map: {},
      places: null,
      markers: [],
      ps: {},
      infowindow: {},
      courses: [],
      users: [
        { x: 127.048584257261, y: 37.5792782282719 },
        { x: 127.04955812811862, y: 37.5713551811832 },
        { x: 127.049986291544086, y: 37.57263296172184 },
        { x: 127.050682513554554, y: 37.57321034054742 },
        { x: 127.051346760004206, y: 37.57235740081413 },
        { x: 127.051346760005218, y: 37.57235740071429 },
      ],
      //   users: [
      //     { x: 126.57159381623066, y: 33.45133510810506 },
      //     { x: 126.5713551811832, y: 33.44955812811862 },
      //     { x: 126.57263296172184, y: 33.449986291544086 },
      //     { x: 126.57321034054742, y: 33.450682513554554 },
      //     { x: 126.57235740081413, y: 33.451346760004206 },
      //   ],
    };
  },
  methods: {
    addScript() {
      const script = document.createElement("script");
      /* global kakao */
      script.onload = () => kakao.maps.load(this.initMap);
      script.src =
        "//dapi.kakao.com/v2/maps/sdk.js?appkey=be80825bde1c9ecb6216babea86cf0ea&autoload=false&libraries=services,clusterer,drawing";
      document.head.appendChild(script);
    },
    initMap() {
      var mapContainer = document.getElementById("map"), // 지도를 표시할 div
        mapOption = {
          center: new kakao.maps.LatLng(33.450701, 126.570667), // 지도의 중심좌표
          level: 3, // 지도의 확대 레벨
        };
      var map = new kakao.maps.Map(mapContainer, mapOption); // 지도를 생성합니다

      // 다각형을 구성하는 좌표 배열입니다. 이 좌표들을 이어서 다각형을 표시합니다
      var polygonPath = [];
      var bounds = new kakao.maps.LatLngBounds();

      for (var i = 0; i < this.users.length; i++) {
        polygonPath.push(
          new kakao.maps.LatLng(this.users[i].y, this.users[i].x)
        );
        bounds.extend(new kakao.maps.LatLng(this.users[i].y, this.users[i].x));
      }

      // 지도에 표시할 다각형을 생성합니다
      var polygon = new kakao.maps.Polygon({
        path: polygonPath, // 그려질 다각형의 좌표 배열입니다
        strokeWeight: 3, // 선의 두께입니다
        strokeColor: "#39DE2A", // 선의 색깔입니다
        strokeOpacity: 0.8, // 선의 불투명도 입니다 1에서 0 사이의 값이며 0에 가까울수록 투명합니다
        strokeStyle: "longdash", // 선의 스타일입니다
        fillColor: "#A2FF99", // 채우기 색깔입니다
        fillOpacity: 0.7, // 채우기 불투명도 입니다
      });

      // 지도에 다각형을 표시합니다
      polygon.setMap(map);
      map.setBounds(bounds);
    },
  },
};
</script>

<style>
</style>