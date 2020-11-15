<template>
  <v-form v-model="valid" class="mb-2">
    <v-container>
      <v-row>
        <v-col cols="12" class="py-0 pl-1">

          <h2 class="page_title">
            <span class="ft-dh bold"> {{ sportsNameKR }} </span>
            <span class="ft-dh bold">매치</span>
            <span class="ft-dh onred bold">온</span>
          </h2>
          <!-- <v-text-field
            v-model="sportsNameKR"
            label="매치 종목은"
            readonly
            color="rgb(189, 22, 44)"
          ></v-text-field> -->
        </v-col>

        <v-col cols="12" class="py-0">
          <v-menu
            v-model="menu1"
            :close-on-content-click="false"
            :nudge-right="0"
            transition="scale-transition"
            offset-y
            min-width="290px"
          >
            <template v-slot:activator="{ on, attrs }">
              <v-text-field
                v-model="date1"
                label="매치를 원하는 날짜를 선택하세요"
                readonly
                v-bind="attrs"
                v-on="on"
                color="rgb(189, 22, 44)"
              ></v-text-field>
            </template>
            <v-date-picker
              color="rgba(189, 22, 44)"
              v-model="date1"
              @input="menu1 = false"
              :min="today"
              locale="kr"
            ></v-date-picker>
          </v-menu>
        </v-col>

        <v-col cols="12" class="py-0 mt-1">
          <div class="mb-0" style="font-size: 12px">
            매치 가능한 시간을 선택하세요.
          </div>
          <div>
            <p class="mb-0">
              <span class="bold">{{ (time[0] + 6) | ChangeTime }}시</span>부터
              <span class="bold">{{ (time[1] + 6) | ChangeTime }}시</span>사이
            </p>
          </div>
          <v-range-slider
            v-model="time"
            :tick-labels="ticksLabels"
            :max="16"
            step="1"
            ticks="always"
            tick-size="3"
            color="rgb(189, 22, 44)"
          >
          </v-range-slider>
        </v-col>
        <div class="mx-3 mb-1" style="font-size: 12px">
          매치를 원하는 위치에 마커를 설정해주세요.
        </div>
        <div id="map" style="margin: auto; width: 95%; height: 270px"></div>

        <v-col cols="12" class="text-center">
          <v-btn
            style="text-transform: none"
            color="rgb(189, 22, 44)"
            dark
            class="py-2 mt-1"
            width="200px"
            @click="submit(sportsNameKR, date1, time)"
          >
            한 판 붙자!
          </v-btn>
        </v-col>
      </v-row>
      <!-- <p>{{ sportsName }}</p>
      <p>{{ date1 }}</p>
      <p>{{ time }}</p> -->
      <v-snackbar v-model="alert_collide">
        이미 같은 시간에 등록된 다른 경기가 있습니다. <br />
        다른 시간을 선택해주세요.
        <template v-slot:action="{ attrs }">
          <v-btn
            color="pink"
            text
            v-bind="attrs"
            @click="alert_collide = false"
          >
            닫기
          </v-btn>
        </template>
      </v-snackbar>
    </v-container>
  </v-form>
</template>

<script>
import MapPin from "@/assets/images/mics/map-pin.png";

import http from "@/util/http-common";
import { mapState } from "vuex";
import axios from "axios";

export default {
  name: "About",
  components: {},
  data() {
    return {
      alert_collide: false,
      sportsName: this.$route.query.sports,
      sportsNameKR: this.$route.query.sportsKR,
      menu1: false,
      date1: "",
      time: [0, 1],
      ticksLabels: [
        "오전 6시",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "오후 10시",
      ],
      today: "",
      lat: "37.5663",
      lng: "126.9779",
      marker1: "",
    };
  },
  computed: {
    ...mapState(["token"]),
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
      var self = this;
      var mapContainer = document.getElementById("map"), // 지도를 표시할 div
        mapOption = {
          center: new kakao.maps.LatLng(33.450701, 126.570667), // 지도의 중심좌표
          level: 3, // 지도의 확대 레벨
        };
      var map = new kakao.maps.Map(mapContainer, mapOption); // 지도를 생성합니다

      var self = this;
      var myx;
      var myy;
      if (navigator.geolocation) {
        // GeoLocation을 이용해서 접속 위치를 얻어옵니다
        navigator.geolocation.getCurrentPosition((position) => {
          var lat1 = position.coords.latitude, // 위도
            lon1 = position.coords.longitude; // 경도
          self.lng = lon1;
          self.lat = lat1;

          console.log("지오로케이션으로 받아온 현재 위치", self.lng, self.lat);

          var locPosition = new kakao.maps.LatLng(lat1, lon1); // 마커가 표시될 위치를 geolocation으로 얻어온 좌표로 생성합니다

          // 마커와 인포윈도우를 표시합니다
          displayMarker(locPosition);
        });
      } else {
        // HTML5의 GeoLocation을 사용할 수 없을때 마커 표시 위치와 인포윈도우 내용을 설정합니다

        var locPosition = new kakao.maps.LatLng(33.450701, 126.570667);
        alert("현재 위치를 받아올 수 없어요");

        displayMarker(locPosition);
      }

      // 지도에 마커와 인포윈도우를 표시하는 함수입니다
      function displayMarker(locPosition) {
        // 마커를 생성합니다

        var imageSrc = MapPin,
          imageSize = new kakao.maps.Size(30, 45);
        var markerImage = new kakao.maps.MarkerImage(imageSrc, imageSize);

        var marker = new kakao.maps.Marker({
          map: map,
          position: locPosition,
          image: markerImage,
        });

        // 지도 중심좌표를 접속위치로 변경합니다
        map.setCenter(locPosition);

        // 마커가 드래그 가능하도록 설정합니다
        marker.setDraggable(false);

        kakao.maps.event.addListener(map, "dragend", function () {
          // 지도 중심좌표를 얻어옵니다

          var position = map.getCenter();
          marker.setPosition(position);
          self.lng = position.getLng();
          self.lat = position.getLat();
        });

        kakao.maps.event.addListener(map, "zoom_changed", function () {
          // 지도 중심좌표를 얻어옵니다

          var position = map.getCenter();
          marker.setPosition(position);
        });

        // kakao.maps.event.addListener(map, "click", function (mouseEvent) {
        //   // 클릭한 위도, 경도 정보를 가져옵니다
        //   var latlng = mouseEvent.latLng;

        //   // 마커 위치를 클릭한 위치로 옮깁니다
        //   marker.setPosition(latlng);

        //   console.log(latlng.getLat(), latlng.getLng());
        //   self.lng = latlng.getLng();
        //   self.lat = latlng.getLat();

        //   var resultDiv = document.getElementById("clickLatlng");
        // });
      }
    },
    submit(sportsNameKR, date1, time) {
      const requestHeaders = {
        headers: {
          Authorization: "JWT " + this.token,
        },
      };
      const temp_time0 = this.time[0];
      const temp_time1 = this.time[1];
      this.time[0] += 6;
      this.time[1] += 6;
      if (this.time[0] < 10) {
        this.time[0] = "0" + this.time[0];
      }
      if (this.time[1] < 10) {
        this.time[1] = "0" + this.time[1];
      }
      console.log(this.time);
      console.log(sessionStorage.getItem("token2"));
      http
        .post(
          "/match/bm/",
          {
            sports_name: this.sportsName,
            date: this.date1,
            start_time: this.time[0] + ":00",
            end_time: this.time[1] + ":00",
            lat: this.lat,
            lng: this.lng,
            device_token: sessionStorage.getItem("token2"),
          },
          requestHeaders
        )
        .then((res) => {
          if (res.data.status_code == 403) {
            this.alert_collide = true;
            this.time[0] = temp_time0;
            this.time[1] = temp_time1;
          } else {
            console.log(res);
            console.log(res.data.result);
            console.log(typeof res.data.result);
            console.log(Object.keys(res.data).length);
            if (res.data.result === "true") {
              console.log("이프 됨");
              console.log(res.data.device_tokens);
              for (const i in res.data.device_tokens) {
                console.log("for 됨");
                console.log(res.data.device_tokens[i]);
                axios
                  .post(
                    "https://fcm.googleapis.com/fcm/send",
                    {
                      to: res.data.device_tokens[i],
                      data: {
                        message:
                          "매칭이 완료되었습니다! 채팅방에서 경기 시간 및 장소를 조율해주세요.",
                      },
                    },
                    {
                      headers: {
                        "Content-Type": "application/json",
                        Authorization:
                          "key=AAAA5zwJHyg:APA91bGz18YD6un-vpBJDryN8g3PLx7NEbH7ChmnxU4l0TOOx1HKSpNZ7v3td8Fqb67tOHqmXvjnBRCpg_cUYzbGTQs0DZmophlF-gi4hCXMsUBkwQ1LYkE8aPB_eR-R2kQBjZvLmdKU",
                        Accept: "application/json",
                      },
                    }
                  )
                  .then((data) => {
                    console.log("push notification success");
                    console.log(data);
                  })
                  .catch((err) => {
                    console.log("push notification fail");
                    console.log(err);
                  });
              }
            }
            this.$router.push({
              name: "Matching",
              query: { sportsNameKR: sportsNameKR, date1: date1, time: time },
            });
          }
        })
        .catch((err) => {
          console.log(err);
          this.alert_collide = true;
        });
    },
    getToday() {
      var today = new Date();
      var dd = today.getDate();
      var mm = today.getMonth() + 1;
      var yyyy = today.getFullYear();

      if (dd < 10) {
        dd = "0" + dd;
      }

      if (mm < 10) {
        mm = "0" + mm;
      }

      today = yyyy + "-" + mm + "-" + dd;
      this.today = today;
      this.date1 = today;
    },
  },
  mounted() {
    this.getToday();
    window.kakao && window.kakao.maps ? this.initMap() : this.addScript();
  },
  filters: {
    ChangeTime(timeTime) {
      if (timeTime < 12) {
        var newTime = "오전 " + timeTime;
        return newTime;
      } else if (timeTime == 12) {
        var newTime = "오후 " + timeTime;
        return newTime;
      } else if (timeTime > 12) {
        var newTime = "오후 " + (timeTime - 12);
        return newTime;
      }
    },
  },
};
</script>

<style scoped>

.page_title {
  padding-left: 6px;
  padding-right: 10px;
  padding-top: 8px;
  padding-bottom: 6px;
  /* margin-right: 2px; */
  font-size: 30px;
}

</style>