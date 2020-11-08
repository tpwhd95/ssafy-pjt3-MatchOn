<template>
  <div class="maptest">
    <div class="mt-0">당신은 지금: {{ myloc }}</div>
    <div id="map" style="width: 100%; height: 400px"></div>
    <div class="mt-3 ml-3">선택된 장소: {{ selected }}</div>
    <div class="d-flex justify-end">
      <v-btn color="primary" @click="toChat()"> 채팅하기 </v-btn>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      map: {},
      places: null,
      markers: [],
      ps: {},
      infowindow: {},
      location: "답십리동",
      myloc: "",
      selected: "dsbjiaisd",
      users: [
        { x: 127.048584257261, y: 37.5792782282719 },
        { x: 127.04955812811862, y: 37.5713551811832 },
        { x: 127.049986291544086, y: 37.57263296172184 },
        { x: 127.050682513554554, y: 37.57321034054742 },
        { x: 127.051346760004206, y: 37.57235740081413 },
        { x: 127.051346760005218, y: 37.57235740071429 },
      ],

      cenx: 0,
      ceny: 0,
      innerText: "",
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
    getLocation() {
      if (navigator.geolocation) {
        // GPS를 지원하면
        navigator.geolocation.getCurrentPosition(
          (position) => {
            var myx = position.coords.longitude;
            var myy = position.coords.latitude;
            var my_loc = "";
            // 내 위치 찾기
            var geocoder1 = new kakao.maps.services.Geocoder();
            var callback = (result, status) => {
              if (status === kakao.maps.services.Status.OK) {
                my_loc = result[0].address_name;
                console.log(my_loc);
                this.myloc = my_loc;
                // this.my_loc = result[0].address_name.split(" ")[2];
              }
            };

            geocoder1.coord2RegionCode(myx, myy, callback);
          },
          function (error) {
            console.error(error);
          },
          {
            enableHighAccuracy: false,
            maximumAge: 0,
            timeout: Infinity,
          }
        );
      } else {
        alert("GPS를 지원하지 않습니다");
      }
    },
    findcenter() {
      var sumx = 0,
        sumy = 0,
        cenx = 0,
        ceny = 0;
      for (var i = 0; i < this.users.length; i++) {
        sumx += this.users[i].x;
        sumy += this.users[i].y;
      }
      this.cenx = sumx / this.users.length;
      this.ceny = sumy / this.users.length;
    },
    toChat() {
      this.$router.push("/chat");
    },
    addScript() {
      const script = document.createElement("script");
      /* global kakao */
      script.onload = () => kakao.maps.load(this.initMap);
      script.src =
        "//dapi.kakao.com/v2/maps/sdk.js?appkey=be80825bde1c9ecb6216babea86cf0ea&autoload=false&libraries=services,clusterer,drawing";
      document.head.appendChild(script);
    },
    initMap() {
      var self = this;
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

      this.getLocation();

      // 센터 위치 찾기
      var geocoder = new kakao.maps.services.Geocoder();
      var center_loc = "12";
      var callback = function (result, status) {
        if (status === kakao.maps.services.Status.OK) {
          console.log("지역 명칭 : " + result[0].address_name);
          center_loc = result[0].address_name.split(" ")[2];
          console.log(center_loc + " 당구장");
        }
        // 장소 검색 객체를 생성합니다
        var ps = new kakao.maps.services.Places();

        // 키워드로 장소를 검색합니다
        ps.keywordSearch(center_loc + " 당구장", placesSearchCB);
      };

      geocoder.coord2RegionCode(this.cenx, this.ceny, callback);

      var infowindow = new kakao.maps.InfoWindow({ zIndex: 1 });

      function placesSearchCB(data, status, pagination) {
        if (status === kakao.maps.services.Status.OK) {
          // 검색된 장소 위치를 기준으로 지도 범위를 재설정하기위해
          // LatLngBounds 객체에 좌표를 추가합니다
          var bounds = new kakao.maps.LatLngBounds();

          for (var i = 0; i < data.length; i++) {
            displayMarker(data[i]);
            bounds.extend(new kakao.maps.LatLng(data[i].y, data[i].x));
          }

          // 검색된 장소 위치를 기준으로 지도 범위를 재설정합니다
          map.setBounds(bounds);
        }
      }

      // 지도에 마커를 표시하는 함수입니다
      function displayMarker(place) {
        // 마커를 생성하고 지도에 표시합니다
        var marker = new kakao.maps.Marker({
          map: map,
          position: new kakao.maps.LatLng(place.y, place.x),
        });

        // 마커에 클릭이벤트를 등록합니다
        kakao.maps.event.addListener(marker, "click", function () {
          // 마커를 클릭하면 장소명이 인포윈도우에 표출됩니다
          var content =
            '<div class="wrap" style="padding:5px;font-size:12px;background-color:white;width:200px;">' +
            '    <div class="place" style="background-color:white;">' +
            '        <div class="title">' +
            place.place_name +
            '            <div class="close" onclick="closeOverlay()" title="닫기"></div>' +
            "        </div>" +
            '        <div class="body">' +
            '            <div class="desc">' +
            '                <div class="ellipsis">' +
            place.road_address_name +
            "</div>" +
            '                <div class="jibun ellipsis">' +
            place.phone +
            "</div>" +
            '                <div><a href="' +
            place.place_url +
            '" target="_blank" class="link">자세히보기</a></div>' +
            "            </div>" +
            "        </div>" +
            "    </div>" +
            "</div>";
          infowindow.setContent(
            // '<div style="padding:5px;font-size:12px;">' +
            //   place.place_name +
            //   "</div>"
            content
          );
          infowindow.open(map, marker);
          self.selected = place.place_name;
        });
      }

      // 인포윈도우를 닫는 클로저를 만드는 함수입니다
      function makeOutListener(infowindow) {
        return function () {
          infowindow.close();
        };
      }
      function closeOverlay() {
        infowindow.setMap(null);
      }
    },
  },
  mounted() {
    window.kakao && window.kakao.maps ? this.initMap() : this.addScript();
    this.findcenter();
  },
};
</script>

<style scoped>
</style>