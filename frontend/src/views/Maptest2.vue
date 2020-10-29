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
      location: "동대문구",
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

      var infowindow = new kakao.maps.InfoWindow({ zIndex: 1 });
      // 장소 검색 객체를 생성합니다
      var ps = new kakao.maps.services.Places();

      // 키워드로 장소를 검색합니다
      ps.keywordSearch(this.location + "당구장", placesSearchCB);

      function placesSearchCB(data, status, pagination) {
        if (status === kakao.maps.services.Status.OK) {
          // 검색된 장소 위치를 기준으로 지도 범위를 재설정하기위해
          // LatLngBounds 객체에 좌표를 추가합니다
          var bounds = new kakao.maps.LatLngBounds();

          for (var i = 0; i < data.length; i++) {
            // displayMarker(data[i]);
            var gapX = MARKER_WIDTH + SPRITE_GAP, // 스프라이트 이미지에서 마커로 사용할 이미지 X좌표 간격 값
              originY = (MARKER_HEIGHT + SPRITE_GAP) * i, // 스프라이트 이미지에서 기본, 클릭 마커로 사용할 Y좌표 값
              overOriginY = (OVER_MARKER_HEIGHT + SPRITE_GAP) * i, // 스프라이트 이미지에서 오버 마커로 사용할 Y좌표 값
              normalOrigin = new kakao.maps.Point(0, originY), // 스프라이트 이미지에서 기본 마커로 사용할 영역의 좌상단 좌표
              clickOrigin = new kakao.maps.Point(gapX, originY), // 스프라이트 이미지에서 마우스오버 마커로 사용할 영역의 좌상단 좌표
              overOrigin = new kakao.maps.Point(gapX * 2, overOriginY); // 스프라이트 이미지에서 클릭 마커로 사용할 영역의 좌상단 좌표

            // 마커를 생성하고 지도위에 표시합니다
            addMarker(data[i], normalOrigin, overOrigin, clickOrigin);
            bounds.extend(new kakao.maps.LatLng(data[i].y, data[i].x));
          }

          // 검색된 장소 위치를 기준으로 지도 범위를 재설정합니다
          map.setBounds(bounds);
        }
      }

      var MARKER_WIDTH = 33, // 기본, 클릭 마커의 너비
        MARKER_HEIGHT = 36, // 기본, 클릭 마커의 높이
        OFFSET_X = 12, // 기본, 클릭 마커의 기준 X좌표
        OFFSET_Y = MARKER_HEIGHT, // 기본, 클릭 마커의 기준 Y좌표
        OVER_MARKER_WIDTH = 40, // 오버 마커의 너비
        OVER_MARKER_HEIGHT = 42, // 오버 마커의 높이
        OVER_OFFSET_X = 13, // 오버 마커의 기준 X좌표
        OVER_OFFSET_Y = OVER_MARKER_HEIGHT, // 오버 마커의 기준 Y좌표
        SPRITE_MARKER_URL =
          "https://t1.daumcdn.net/localimg/localimages/07/mapapidoc/markers_sprites2.png", // 스프라이트 마커 이미지 URL
        SPRITE_WIDTH = 126, // 스프라이트 이미지 너비
        SPRITE_HEIGHT = 146, // 스프라이트 이미지 높이
        SPRITE_GAP = 10; // 스프라이트 이미지에서 마커간 간격

      var markerSize = new kakao.maps.Size(MARKER_WIDTH, MARKER_HEIGHT), // 기본, 클릭 마커의 크기
        markerOffset = new kakao.maps.Point(OFFSET_X, OFFSET_Y), // 기본, 클릭 마커의 기준좌표
        overMarkerSize = new kakao.maps.Size(
          OVER_MARKER_WIDTH,
          OVER_MARKER_HEIGHT
        ), // 오버 마커의 크기
        overMarkerOffset = new kakao.maps.Point(OVER_OFFSET_X, OVER_OFFSET_Y), // 오버 마커의 기준 좌표
        spriteImageSize = new kakao.maps.Size(SPRITE_WIDTH, SPRITE_HEIGHT); // 스프라이트 이미지의 크기

      // 마커를 생성하고 지도 위에 표시하고, 마커에 mouseover, mouseout, click 이벤트를 등록하는 함수입니다
      function addMarker(position, normalOrigin, overOrigin, clickOrigin) {
        // 기본 마커이미지, 오버 마커이미지, 클릭 마커이미지를 생성합니다
        var normalImage = createMarkerImage(
            markerSize,
            markerOffset,
            normalOrigin
          ),
          overImage = createMarkerImage(
            overMarkerSize,
            overMarkerOffset,
            overOrigin
          ),
          clickImage = createMarkerImage(markerSize, markerOffset, clickOrigin);

        // 마커를 생성하고 이미지는 기본 마커 이미지를 사용합니다
        var marker = new kakao.maps.Marker({
          map: map,
          position: new kakao.maps.LatLng(position.y, position.x),
          image: normalImage,
        });

        // 마커 객체에 마커아이디와 마커의 기본 이미지를 추가합니다
        marker.normalImage = normalImage;

        // 마커에 mouseover 이벤트를 등록합니다
        kakao.maps.event.addListener(marker, "mouseover", function () {
          // 클릭된 마커가 없고, mouseover된 마커가 클릭된 마커가 아니면
          // 마커의 이미지를 오버 이미지로 변경합니다
          if (!selectedMarker || selectedMarker !== marker) {
            marker.setImage(overImage);
          }
          infowindow.setContent(
            '<div style="padding:5px;font-size:12px;">' +
              position.place_name +
              "</div>"
          );
          infowindow.open(map, marker);
        });

        // 마커에 mouseout 이벤트를 등록합니다
        kakao.maps.event.addListener(marker, "mouseout", function () {
          // 클릭된 마커가 없고, mouseout된 마커가 클릭된 마커가 아니면
          // 마커의 이미지를 기본 이미지로 변경합니다
          if (!selectedMarker || selectedMarker !== marker) {
            marker.setImage(normalImage);
          }
          infowindow.close(map, marker);
        });

        // 마커에 click 이벤트를 등록합니다
        kakao.maps.event.addListener(marker, "click", function () {
          // 클릭된 마커가 없고, click 마커가 클릭된 마커가 아니면
          // 마커의 이미지를 클릭 이미지로 변경합니다
          if (!selectedMarker || selectedMarker !== marker) {
            // 클릭된 마커 객체가 null이 아니면
            // 클릭된 마커의 이미지를 기본 이미지로 변경하고
            !!selectedMarker &&
              selectedMarker.setImage(selectedMarker.normalImage);

            // 현재 클릭된 마커의 이미지는 클릭 이미지로 변경합니다
            marker.setImage(clickImage);
          }

          // 클릭된 마커를 현재 클릭된 마커 객체로 설정합니다
          selectedMarker = marker;
        });
      }

      // MakrerImage 객체를 생성하여 반환하는 함수입니다
      function createMarkerImage(markerSize, offset, spriteOrigin) {
        var markerImage = new kakao.maps.MarkerImage(
          SPRITE_MARKER_URL, // 스프라이트 마커 이미지 URL
          markerSize, // 마커의 크기
          {
            offset: offset, // 마커 이미지에서의 기준 좌표
            spriteOrigin: spriteOrigin, // 스트라이프 이미지 중 사용할 영역의 좌상단 좌표
            spriteSize: spriteImageSize, // 스프라이트 이미지의 크기
          }
        );

        return markerImage;
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
          infowindow.setContent(
            '<div style="padding:5px;font-size:12px;">' +
              place.place_name +
              "</div>"
          );
          infowindow.open(map, marker);
        });
      }
    },
  },
};
</script>

<style>
</style>