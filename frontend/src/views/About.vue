<template>
  <v-form v-model="valid">
    <v-container>
      <v-row>
        <v-col cols="12">
          <v-text-field
            v-model="sportsNameKR"
            label="종목"
            readonly
          ></v-text-field>
        </v-col>

        <v-col cols="12">
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
                label="날짜"
                readonly
                v-bind="attrs"
                v-on="on"
              ></v-text-field>
            </template>
            <v-date-picker
              v-model="date1"
              @input="menu1 = false"
              :min="today"
            ></v-date-picker>
          </v-menu>
        </v-col>

        <v-col cols="12">
          <v-range-slider
            v-model="time"
            :tick-labels="ticksLabels"
            :max="16"
            step="1"
            ticks="always"
            tick-size="3"
          ></v-range-slider>
        </v-col>
        <v-col cols="12" class="d-flex justify-center">
          <v-btn
            style="text-transform: none"
            color="primary"
            dark
            @click="submit(sportsNameKR, date1, time)"
          >
            MatchOn!
          </v-btn>
        </v-col>
      </v-row>
      <!-- <p>{{ sportsName }}</p>
      <p>{{ date1 }}</p>
      <p>{{ time }}</p> -->
    </v-container>
  </v-form>
</template>

<script>
import http from "@/util/http-common";
import { mapState } from "vuex";
import axios from "axios";

export default {
  name: "About",
  components: {},
  data() {
    return {
      sportsName: this.$route.params.sports,
      sportsNameKR: this.$route.params.sportsKR,
      menu1: false,
      date1: "",
      time: [0, 1],
      ticksLabels: [
        6,
        7,
        8,
        9,
        10,
        11,
        12,
        13,
        14,
        15,
        16,
        17,
        18,
        19,
        20,
        21,
        22,
      ],
      today: "",
      lat: "37.5663",
      lng: "126.9779",
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
    },
    getLocation() {
      var self = this;
      if (navigator.geolocation) {
        // GPS를 지원하면
        navigator.geolocation.getCurrentPosition(
          (position) => {
            var myx = position.coords.longitude;
            var myy = position.coords.latitude;
            self.lng = myx;
            self.lat = myy;
            console.log(self.lng, self.lat);
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
    submit(sportsNameKR, date1, time) {
      const requestHeaders = {
        headers: {
          Authorization: "JWT " + this.token,
        },
      };
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
        })
        .catch((err) => {
          console.log(err);
        });
      this.$router.push({
        name: "Matching",
        params: { sportsNameKR: sportsNameKR, date1: date1, time: time },
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
    this.getLocation();
  },
};
</script>

<style>
</style>