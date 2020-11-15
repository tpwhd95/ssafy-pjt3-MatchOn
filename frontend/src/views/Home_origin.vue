<template>
  <div class="h-100">
    <v-container
      v-if="!this.isLoggedIn"
      class="h-100 mx-auto d-flex justify-center align-center pb-15 bg-brown"
      max-width="720"
    >
      <div class="text-center">
        <h2 class="main-text ft-dh mb-7">
          온라인 스포츠 <span class="ft-dh onred bold"> 매칭 </span>서비스
        </h2>
        <img
          src="@/assets/images/logos/full_logo_black.png"
          alt="match-on-logo"
          style="height: 150px"
          class="mb-7"
        />
        <h3 class="main-text">서비스 사용을 위해 로그인해주세요</h3>
      </div>
    </v-container>

    <!-- 비 로그인 디비전 끝! -->

    <!-- 로그인 디비전 -->
    <!-- 현재 매칭 정보 -->
    <v-card
      v-if="this.isLoggedIn && this.flag == false"
      class="mx-auto"
      max-width="720"
    >
      <v-container fluid>
        <h2>{{ userProfile.username }}님의 경기 정보</h2>
        <v-row>
          <v-col v-for="card1 in cards1" :key="card1.title" :cols="card1.flex">
            <v-card style="padding: 16px">
              <h3>{{ card1.title }}</h3>
              <v-row>
                <v-col
                  v-for="card2 in card1.cards2"
                  :key="card2.sports"
                  :cols="card2.flex"
                >
                  <v-card
                    v-if="card1.title == '조율중인 경기'"
                    style="padding: 8px"
                    @click="getMatchRoom(card2.match_pk)"
                  >
                    <p style="margin: 12px 0px">종목: {{ card2.sports }}</p>
                    <p style="margin: 12px 0px">날짜: {{ card2.date }}</p>
                    <p style="margin: 12px 0px">
                      시간: {{ card2.match_start | ChangeTime }}시 ~
                      {{ card2.match_end | ChangeTime }}시
                    </p>
                  </v-card>

                  <v-card
                    v-if="card1.title == '대기중인 경기'"
                    style="padding: 8px"
                  >
                    <p style="margin: 12px 0px">종목: {{ card2.sports }}</p>
                    <p style="margin: 12px 0px">날짜: {{ card2.date }}</p>
                    <p style="margin: 12px 0px">
                      시간: {{ card2.fixed_time | ChangeTime }}시
                    </p>
                  </v-card>

                  <v-card
                    v-if="card1.title == '진행중인 경기'"
                    style="padding: 8px"
                    @click="
                      getResultRoom(
                        card2.match_pk,
                        card2.sports,
                        card2.date,
                        card2.fixed_time
                      )
                    "
                  >
                    <p style="margin: 12px 0px">종목: {{ card2.sports }}</p>
                    <p style="margin: 12px 0px">날짜: {{ card2.date }}</p>
                    <p style="margin: 12px 0px">
                      시간: {{ card2.fixed_time | ChangeTime }}시
                    </p>
                  </v-card>
                </v-col>
              </v-row>
            </v-card>
          </v-col>
        </v-row>
      </v-container>
    </v-card>

    <!-- 매칭 신청 -->
    <v-card v-if="this.isLoggedIn" class="mx-auto" max-width="720">
      <v-container fluid>
        <v-row>
          <v-col
            v-for="card in cards"
            :key="card.title"
            :cols="card.flex"
            :sportsName="card.title"
          >
            <v-card>
              <v-img
                :src="card.src"
                class="white--text align-end"
                gradient="to bottom, rgba(0,0,0,.1), rgba(0,0,0,.5)"
                height="200px"
                @click="matching(card.title, card.title2)"
                style="cursor: pointer"
              >
                <v-card-title v-text="card.title2"></v-card-title>
              </v-img>
            </v-card>
          </v-col>
        </v-row>
      </v-container>
    </v-card>
  </div>
</template>

<script>
import http from "@/util/http-common";
import { mapGetters, mapState } from "vuex";

export default {
  name: "Home",
  components: {},
  data() {
    return {
      flag: true,
      sportsName: "",
      cards: [
        {
          title: "futsal",
          title2: "풋살",
          src: require("@/assets/images/sports/futsal.jpg"),
          flex: 12,
        },
        {
          title: "basket_ball",
          title2: "농구",
          src: require("@/assets/images/sports/basketball.jpg"),
          flex: 12,
        },
        {
          title: "tennis",
          title2: "테니스",
          src: require("@/assets/images/sports/tennis.jpg"),
          flex: 12,
        },
        {
          title: "pool",
          title2: "당구",
          src: require("@/assets/images/sports/pool.jpg"),
          flex: 12,
        },
        {
          title: "bowling",
          title2: "볼링",
          src: require("@/assets/images/sports/bowling.jpg"),
          flex: 12,
        },
      ],

      userProfile: sessionStorage.getItem("userProfile")
        ? JSON.parse(sessionStorage.getItem("userProfile"))
        : [],
      cards1: [
        // {
        //   title: "매칭중인 경기",
        //   flex: 12,
        //   cards2: [],
        // },
        {
          title: "조율중인 경기",
          flex: 12,
          cards2: [],
        },
        {
          title: "대기중인 경기",
          flex: 12,
          cards2: [],
        },
        {
          title: "진행중인 경기",
          flex: 12,
          cards2: [],
        },
        // {
        //   title: "완료된 경기",
        //   flex: 12,
        //   cards2: [],
        // },
      ],
    };
  },
  methods: {
    matching(sportsName, sportsNameKR) {
      this.$router.push({
        name: "About",
        query: { sports: sportsName, sportsKR: sportsNameKR },
      });
    },

    getMatchInfo() {
      console.log(this.token);
      const self = this;
      http
        .get("/auth/match-info/", {
          headers: {
            Authorization: "JWT " + this.token,
          },
        })
        .then(function (res) {
          console.log(res);
          for (let i of res.data.data) {
            // if (i.status == 1) {
            //   var temp_sports = "";
            //   if (i.sports_name == "futsal") {
            //     temp_sports = "풋살";
            //   }
            //   if (i.sports_name == "basket_ball") {
            //     temp_sports = "농구";
            //   }
            //   if (i.sports_name == "pool") {
            //     temp_sports = "당구";
            //   }
            //   if (i.sports_name == "tennis") {
            //     temp_sports = "테니스";
            //   }
            //   if (i.sports_name == "bowling") {
            //     temp_sports = "볼링";
            //   }
            //   self.cards1[0].cards2.push({
            //     sports: temp_sports,
            //     date: i.date,
            //     flex: 12,
            //     start_time: i.start_time,
            //     end_time: i.end_time,
            //   });
            // }
            if (i.status == 2) {
              self.flag = false;
              var temp_sports = "";
              if (i.sports_name == "futsal") {
                temp_sports = "풋살";
              }
              if (i.sports_name == "basket_ball") {
                temp_sports = "농구";
              }
              if (i.sports_name == "pool") {
                temp_sports = "당구";
              }
              if (i.sports_name == "tennis") {
                temp_sports = "테니스";
              }
              if (i.sports_name == "bowling") {
                temp_sports = "볼링";
              }
              self.cards1[0].cards2.push({
                sports: temp_sports,
                date: i.date,
                flex: 12,
                match_pk: i.matching_pk,
                match_start: i.match_start,
                match_end: i.match_end,
              });
            }
            if (i.status == 3) {
              self.flag = false;
              var temp_sports = "";
              if (i.sports_name == "futsal") {
                temp_sports = "풋살";
              }
              if (i.sports_name == "basket_ball") {
                temp_sports = "농구";
              }
              if (i.sports_name == "pool") {
                temp_sports = "당구";
              }
              if (i.sports_name == "tennis") {
                temp_sports = "테니스";
              }
              if (i.sports_name == "bowling") {
                temp_sports = "볼링";
              }
              self.cards1[1].cards2.push({
                sports: temp_sports,
                date: i.date,
                flex: 12,
                fixed_time: i.fixed_time,
              });
            }
            if (i.status == 4) {
              self.flag = false;
              var temp_sports = "";
              if (i.sports_name == "futsal") {
                temp_sports = "풋살";
              }
              if (i.sports_name == "basket_ball") {
                temp_sports = "농구";
              }
              if (i.sports_name == "pool") {
                temp_sports = "당구";
              }
              if (i.sports_name == "tennis") {
                temp_sports = "테니스";
              }
              if (i.sports_name == "bowling") {
                temp_sports = "볼링";
              }
              self.cards1[2].cards2.push({
                sports: temp_sports,
                date: i.date,
                flex: 12,
                fixed_time: i.fixed_time,
                match_pk: i.matching_pk,
              });
            }
            // if (i.status == 5) {
            //   self.flag = false;
            //   var temp_sports = "";
            //   if (i.sports_name == "futsal") {
            //     temp_sports = "풋살";
            //   }
            //   if (i.sports_name == "basket_ball") {
            //     temp_sports = "농구";
            //   }
            //   if (i.sports_name == "pool") {
            //     temp_sports = "당구";
            //   }
            //   if (i.sports_name == "tennis") {
            //     temp_sports = "테니스";
            //   }
            //   if (i.sports_name == "bowling") {
            //     temp_sports = "볼링";
            //   }
            //   self.cards1[3].cards2.push({
            //     sports: temp_sports,
            //     date: i.date,
            //     flex: 12,
            //     fixed_time: i.fixed_time,
            //   });
            // }
          }
        })
        .catch(function (err) {
          alert(err);
        });
    },
    getMatchRoom(match_id) {
      console.log(match_id);
      console.log(this.token);
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
          console.log(res);
        })
        .catch((err) => {
          console.log(err);
        });
      this.$router.push({
        name: "MatchRoom",
        query: { match_id: match_id },
      });
    },
    getResultRoom(match_id, sports, date, time) {
      console.log(match_id);
      console.log(this.token);
      this.$router.push({
        name: "ResultRoom",
        query: { match_id: match_id, sports: sports, date: date, time: time },
      });
    },
  },
  computed: {
    ...mapGetters(["isLoggedIn"]),
    ...mapState(["token"]),
  },
  created() {
    if (this.isLoggedIn) {
      this.getMatchInfo();
    }
  },
  filters: {
    ChangeTime(value) {
      return value.split(":")[0];
    },
  },
};
</script>

<style scoped>
.h-100 {
  height: 100%;
}

.bg-brown {
  background-color: rgba(32, 32, 32, 0.925);
}

.main-text {
  color: rgba(255, 255, 255, 0.863);
}

/* #content {
  position: relative;
  background-color: rgba(0, 1, 41, 0.774);
  width: 100vw;
  height: 100vh;
}

#content:after {
  background-image: url("~@/assets/images/mics/mobile-bg.jpg");

  background-attachment: fixed;
  background-position: center;
  background-size: cover;

  content: "";
  display: block;
  position: absolute;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  z-index: -1;
} */
</style>