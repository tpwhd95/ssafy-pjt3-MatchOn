<template>
  <v-card class="mx-auto mb-14 mt-3" max-width="720">
    <h1 class="ft-dh text-center">
      <span class="ft-dh onred">매치</span><span class="ft-dh">룸</span>
    </h1>
    <!-- 팀원분기 -->
    <div class="mx-2 mt-2">
      <div v-if="userProfile.id == room_master">
        <h3>{{ users[room_master]["username"] }}님이 매치 마스터입니다.</h3>
        <p style="font-size: 12px">
          팀원들과 자유롭게 대화하고 장소와 시간을 정해주세요!
        </p>
      </div>
      <div v-else>
        <h3>매치 마스터는 {{ users[room_master]["username"] }}님입니다.</h3>
        <p style="font-size: 12px">
          팀원들과 자유롭게 대화하고 장소와 시간을 정해주세요!
        </p>
      </div>
    </div>

    <!-- 채팅방 -->
    <v-card
      outlined
      class="messages mx-2 mt-2"
      v-chat-scroll="{ always: false, smooth: true }"
      style="background-color: rgba(0, 0, 0, 0.2)"
    >
      <div v-for="message in messages" :key="message.id">
        <div v-if="message.name == userProfile.username">
          <div class="d-flex justify-end">
            <span class="mx-3" style="color: rgba(0, 0, 0, 0.8)">{{
              message.message
            }}</span>
            <!-- <span class="text-info">:[나] </span> -->
          </div>
          <p
            class="d-flex justify-end text-secondary time mx-3 mb-1 0.5rem"
            style="color: rgba(0, 0, 0, 0.5)"
          >
            {{ message.timestamp }}
          </p>
        </div>
        <div v-else>
          <span class="text-info">[{{ message.name }}]: </span>
          <span>{{ message.message }}</span>
          <br />
          <span class="text-secondary time">{{ message.timestamp }}</span>
        </div>
      </div>
    </v-card>

    <div class="card-action">
      <CreateMessage :name="userProfile.username" :match_id="match_id" />
    </div>

    <p class="ml-2 mb-0" style="font-size: 14px">매치 위치를 선택해주세요.</p>
    <div
      id="map"
      class="mb-10"
      style="margin: auto; width: 95%; height: 270px"
    ></div>
    <div class="card">
      <div class="card-body">
        <p class="text-secondary nomessages" v-if="messages.length == 0">
          [팀원들과 자유롭게 대화하고 방장님은 장소와 시간을 정해주세요!]
        </p>
      </div>

      <!-- <v-row style="margin: 10px">
        <v-checkbox
          v-for="(user, key) in users"
          :key="user.username"
          v-model="teamA"
          :label="user.username"
          :value="key"
        ></v-checkbox>
      </v-row>
      <p>{{ teamA }}</p>
      <p>{{ teamB }}</p>
      <p>{{ fixed_users }}</p> -->
      <p class="ml-4 my-0" v-if="stime != etime">
        매치 가능시간은 {{ stime | ChangeTime }}시부터
        {{ etime | ChangeTime }}시입니다.
      </p>
      <p class="ml-4 my-0" v-if="stime == etime">
        매치 가능시간은 {{ stime | ChangeTime }}시입니다.
      </p>

      <v-row v-if="userProfile.id == room_master" class="mx-1">
        <v-col cols="11" class="py-0">
          <p style="font-size: 12px">매치 시간을 지정해주세요.</p>
          <v-slider
            v-model="ex3.val"
            :label="ex3.label"
            :thumb-color="ex3.color"
            :min="stime"
            :max="etime"
            step="1"
            thumb-label="true"
          ></v-slider>
        </v-col>
      </v-row>
      <div class="text-center">
        <v-btn
          class="mb-2"
          color="rgb(189, 22, 44)"
          v-if="userProfile.id == room_master"
          @click="inputAfterMatch"
        >
          <span style="color: white"> 매치온! </span>
        </v-btn>
      </div>
    </div>
  </v-card>
</template>

<script>
import http from "@/util/http-common";
import { mapState } from "vuex";
import CreateMessage from "@/components/CreateMessage";
import fb from "@/firebase/init";
import moment from "moment";
import MapPin from "@/assets/images/mics/map-pin.png";

export default {
  name: "MatchRoom",
  components: {
    CreateMessage,
  },
  data() {
    return {
      match_id: this.$route.query.match_id,
      room_master: null,
      sport: "",
      start_time: "",
      end_time: "",
      stime: "",
      etime: "",
      center_lat: "37.477107637586194",
      center_lng: "126.96346058714246",
      messages: [],
      userProfile: sessionStorage.getItem("userProfile")
        ? JSON.parse(sessionStorage.getItem("userProfile"))
        : [],
      users_pk: [],
      selected: "",
      fixed_lat: "37.477107637586194",
      fixed_lng: "126.96346058714246",
      ex3: { label: "매치시간", val: 0, color: "red" },
      match_results_ref: null,
      match_users_ref: null,
      fixed_users: {},
    };
  },
  computed: {
    ...mapState(["token"]),
  },
  mounted() {
    this.getRoomData(this.match_id);

    let ref = fb
      .collection("messages" + String(this.match_id))
      .orderBy("timestamp");

    ref.onSnapshot((snapshot) => {
      snapshot.docChanges().forEach((change) => {
        if ((change.type = "added")) {
          let doc = change.doc;
          this.messages.push({
            id: doc.id,
            name: doc.data().name,
            message: doc.data().message,
            timestamp: moment(doc.data().timestamp).format("LTS"),
          });
        }
      });
    });

    this.room_results_ref.onSnapshot((snapshot) => {
      snapshot.docChanges().forEach((change) => {
        if (change.type === "added") {
          console.log("confirmed");
        }
      });
    });
  },
  methods: {
    getRoomData(match_id) {
      http
        .post(
          "/match/match-room/",
          { match_pk: match_id },
          {
            headers: {
              Authorization: "JWT " + this.token,
            },
          }
        )
        .then((res) => {
          this.room_master = Object.keys(res.data.data[0].users)[0];
          this.center_lat = res.data.data[0].match_lat;
          this.center_lng = res.data.data[0].match_lng;
          this.users = res.data.data[0].users;
          this.start_time = res.data.data[0].start_time;
          this.end_time = res.data.data[0].end_time;

          var stime = this.start_time.split(":")[0];
          var etime = this.end_time.split(":")[0];

          this.stime = stime;
          this.etime = etime;

          let users = JSON.parse(JSON.stringify(res.data.data[0].users));
          let user_keys = Object.keys(users);
          const room_users_ref = fb.collection(
            "room_users" + String(this.match_id)
          );
          const room_results_ref = fb.collection(
            "room_results" + String(this.match_id)
          );
          room_users_ref
            .doc(user_keys[0])
            .get()
            .then((doc) => {
              if (this.userProfile.id == user_keys[0] && !doc.exists) {
                // 파이어베이스에 roomid로 룸을 생성하고 하위에 users를 입력
                for (let i = 0; i < user_keys.length; i += 1) {
                  room_users_ref
                    .doc(user_keys[i])
                    .set({
                      user: users[user_keys[i]],
                      user_id: user_keys[i],
                    })
                    .catch((err) => {
                      console.log(err);
                    });
                }
              }
            });
          room_results_ref
            .doc(users[this.userProfile.id].team ? "1" : "0")
            .set({
              match_result: -1,
            })
            .then(() => {
              room_results_ref.onSnapshot((snapshot) => {
                snapshot.docChanges().forEach((change) => {
                  if (change.type === "modified") {
                    this.$router.push("/matchtrue");
                  }
                });
              });
              const users_pk = Object.keys(res.data.data[0].users);
              for (const user_pk of users_pk) {
                if (this.users[user_pk].team == true) {
                  this.fixed_users[user_pk] = { team: 1 };
                } else {
                  this.fixed_users[user_pk] = { team: 0 };
                }
              }
              if (res.data.data[0].sports === "tennis") {
                this.sport = "테니스장";
              } else if (res.data.data[0].sports === "bowling") {
                this.sport = "볼링장";
              } else if (res.data.data[0].sports === "pool") {
                this.sport = "당구장";
              } else if (res.data.data[0].sports === "futsal") {
                this.sport = "풋살장";
              } else if (res.data.data[0].sports === "basket_ball") {
                this.sport = "농구장";
              }
            })
            .then(() => {
              window.kakao && window.kakao.maps
                ? this.initMap()
                : this.addScript();
            });
        })
        .catch((err) => {
          console.log(err);
        });
    },
    inputAfterMatch() {
      if (this.ex3.val < 10) {
        this.ex3.val = "0" + String(this.ex3.val) + ":00:00";
      } else {
        this.ex3.val = String(this.ex3.val) + ":00:00";
      }
      http
        .post(
          "/match/am/",
          {
            match_pk: this.match_id,
            fixed_time: this.ex3.val,
            // fixed_time: "09:00:00",
            users: this.fixed_users,
            fixed_lat: this.fixed_lat,
            fixed_lng: this.fixed_lng,
          },
          {
            headers: {
              Authorization: "JWT " + this.token,
            },
          }
        )
        .then((res) => {
          const room_results_ref = fb.collection(
            "room_results" + String(this.match_id)
          );
          room_results_ref.get().then((querySnapshot) => {
            querySnapshot.forEach((doc) => {
              doc.ref.set({
                match_result: 0,
              });
            });
          });
        })
        .catch((err) => {
          console.log(err);
        });
      // } else {
      //   alert("각 팀의 인원 수가 같아야 합니다.");
      // }
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

      // var locPosition = new kakao.maps.LatLng(self.center_lat, self.center_lng);
      // map.setCenter(locPosition);

      // 다각형을 구성하는 좌표 배열입니다. 이 좌표들을 이어서 다각형을 표시합니다
      var polygonPath = [];
      var bounds = new kakao.maps.LatLngBounds();

      for (var i = 0; i < this.users.length; i++) {
        polygonPath.push(
          new kakao.maps.LatLng(this.users[i].lat, this.users[i].lng)
        );
        bounds.extend(
          new kakao.maps.LatLng(this.users[i].lat, this.users[i].lng)
        );
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

      // 센터 위치 찾기
      var geocoder = new kakao.maps.services.Geocoder();
      var center_loc = "12";
      var callback = (result, status) => {
        if (status === kakao.maps.services.Status.OK) {;
          center_loc = result[0].address_name.split(" ")[2];
        }
        // 장소 검색 객체를 생성합니다
        var ps = new kakao.maps.services.Places();

        // 키워드로 장소를 검색합니다
        ps.keywordSearch(center_loc + " " + self.sport, placesSearchCB);
      };
      geocoder.coord2RegionCode(self.center_lng, self.center_lat, callback);

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
        var imageSrc = MapPin,
          imageSize = new kakao.maps.Size(20, 30);
        var markerImage = new kakao.maps.MarkerImage(imageSrc, imageSize);

        var marker = new kakao.maps.Marker({
          map: map,
          position: new kakao.maps.LatLng(place.y, place.x),
          image: markerImage,
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
          self.fixed_lng = place.x;
          self.fixed_lat = place.y;
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
  filters: {
    ChangeTime(time) {
      if (time < 12) {
        var changedTime = "오전" + time;
        return changedTime;
      } else if (time == 12) {
        var changedTime = "오후" + time;
        return changedTime;
      } else {
        var changedTime = "오후" + (time - 12);
        return changedTime;
      }
    },
  },
  // watch: {
  //   teamA(values) {
  //     if (values.length == this.users_pk.length / 2) {
  //       this.teamB = this.users_pk.filter((item) => !values.includes(item));
  //     } else {
  //       this.teamB = [];
  //     }
  //     for (const user_pk of this.users_pk) {
  //       if (values.includes(user_pk)) {
  //         this.fixed_users[user_pk] = { team: 0 };
  //       } else {
  //         this.fixed_users[user_pk] = { team: 1 };
  //       }
  //     }
  //   },
  // },
};
</script>

<style scoped>
.chat h2 {
  font-size: 2.6em;
  margin-bottom: 0px;
}

.chat h5 {
  margin-top: 0px;
  margin-bottom: 40px;
}

.chat span {
  font-size: 1.2em;
}

.chat .time {
  display: block;
  font-size: 0.7em;
}

.messages {
  max-height: 300px;
  overflow: auto;
}
</style>