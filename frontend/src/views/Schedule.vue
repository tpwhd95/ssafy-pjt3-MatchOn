<template>
  <div class="mb-25">
    <v-card class="mx-auto" max-width="720">
      <v-container fluid>
        <div>
          <v-sheet tile height="54" class="d-flex">
            <div class="page_title">
              <span class="ft-dh bold">{{ userProfile.username }}님의 </span>
              <span class="ft-dh bold">매치</span>
              <span class="ft-dh onred bold">온</span>
            </div>
            <v-btn
              icon
              class="ml-3 mr-1 my-2"
              color="#660C00"
              @click="$refs.calendar.prev()"
            >
              <v-icon>mdi-chevron-left</v-icon>
            </v-btn>
            <v-toolbar-title v-if="$refs.calendar" class="month_title">
              {{ $refs.calendar.title.split(" ")[0] }}
            </v-toolbar-title>

            <v-btn
              icon
              color="#660C00"
              class="ml-1 my-2"
              @click="$refs.calendar.next()"
            >
              <v-icon>mdi-chevron-right</v-icon>
            </v-btn>
          </v-sheet>
          <v-sheet height="480">
            <v-calendar
              color="error"
              ref="calendar"
              v-model="value"
              :weekdays="weekday"
              :type="type"
              :events="events"
              :event-overlap-mode="mode"
              :event-overlap-threshold="30"
              :event-color="getEventColor"
              @change="getEvents"
            ></v-calendar>
          </v-sheet>
        </div>

        <div>
          <h2 class="page_title mt-2">
            <span class="ft-dh">확정된 경기</span>
          </h2>
          <v-slide-group
            v-if="confirmedMatch.cards2 && confirmedMatch.cards2.length"
            active-class="success"
          >
            <v-slide-item v-for="card2 in confirmedMatch.cards2" :key="card2">
              <div class="mr-2 ml-1 mb-3">
                <v-card>
                  <v-img class="card_image" :src="card2.matchSrc">
                    <v-list-item>
                      <v-list-item-content class="pt-3 pb-4">
                        <v-list-item-title class="mytitle">{{
                          card2.sports
                        }}</v-list-item-title>
                        <v-list-item-subtitle class="mysubtitle">{{
                          card2.gu
                        }}</v-list-item-subtitle>
                        <!-- <v-list-item-content class="mysubtitle2">{{ card2.fixed_time | ChangeTime }}시 -->
                        <!-- 매치</v-list-item-content> -->
                      </v-list-item-content>
                    </v-list-item>

                    <v-card-subtitle class="ft-dh mx-0 my-0 pb-0">{{
                      card2.date | ChangeDate
                    }}</v-card-subtitle>

                    <v-card-subtitle class="ft-dh mx-0 my-0 py-0"
                      >{{ card2.fixed_time | ChangeTime }}시
                      매치</v-card-subtitle
                    >
                  </v-img>
                </v-card>
              </div>
            </v-slide-item>
          </v-slide-group>

          <v-card class="ml-1 mr-1 mb-3 noItem" v-else>
            <div class="noMatch">
              <p>아직 확정 된 경기가 없습니다!</p>
            </div>
          </v-card>
        </div>

        <div>
          <v-row justify="center">
            <v-expansion-panels
              accordion
              class="mb-1 mt-2 ft-dh accordion_card"
            >
              <v-expansion-panel v-for="card1 in cards1" :key="card1">
                <v-expansion-panel-header expand-icon="mdi-menu-down">
                  {{ card1.title }}
                </v-expansion-panel-header>
                <v-expansion-panel-content>
                  <v-slide-group active-class="success">
                    <v-slide-item v-for="card2 in card1.cards2" :key="card2">
                      <v-card v-if="card2.status == 1" class="ml-1 mr-1">
                        <v-img class="semi_card_image" :src="card2.matchSrc">
                          <v-card-title>{{ card2.sports }}</v-card-title>
                          <v-card-subtitle>{{ card2.gu }}</v-card-subtitle>
                          <v-list-item>
                            <v-list-item-content class="pt-3 pb-1">
                              <v-list-item-title class="mytitle">{{
                                card2.date | ChangeDate
                              }}</v-list-item-title>
                              <v-list-item-subtitle class="mysubtitle">
                                매치 가능 시간:
                                {{ card2.start_time | ChangeTime }}시 ~
                                {{ card2.end_time | ChangeTime }}시
                              </v-list-item-subtitle>
                            </v-list-item-content>
                          </v-list-item>
                        </v-img>
                      </v-card>

                      <v-card
                        v-else-if="card2.status == 2"
                        class="ml-1 mr-1"
                        @click="getMatchRoom(card2.match_pk)"
                      >
                        <v-img class="semi_card_image" :src="card2.matchSrc">
                          <v-row>
                            <v-col cols="9">
                              <v-card-title>{{ card2.sports }}</v-card-title>
                            </v-col>
                            <v-col cols="3" class="pt-7">
                              <v-chip color="black" dark>click</v-chip>
                            </v-col>
                          </v-row>
                          <v-card-subtitle class="py-0">{{
                            card2.gu
                          }}</v-card-subtitle>
                          <v-list-item>
                            <v-list-item-content class="pt-3 pb-1">
                              <v-list-item-title class="mytitle">{{
                                card2.date | ChangeDate
                              }}</v-list-item-title>
                              <v-list-item-subtitle class="mysubtitle">
                                매치 조율 시간:
                                {{ card2.match_start | ChangeTime }}시 ~
                                {{ card2.match_end | ChangeTime }}시
                              </v-list-item-subtitle>
                            </v-list-item-content>
                          </v-list-item>
                        </v-img>
                      </v-card>

                      <v-card
                        v-else-if="card2.status == 4"
                        class="ml-1 mr-1"
                        @click="
                          getResultRoom(
                            card2.match_pk,
                            card2.sports,
                            card2.date,
                            card2.fixed_time
                          )
                        "
                      >
                        <v-img class="semi_card_image" :src="card2.matchSrc">
                          <v-row>
                            <v-col cols="9">
                              <v-card-title>{{ card2.sports }}</v-card-title>
                            </v-col>
                            <v-col cols="3" class="pt-7">
                              <v-chip color="black" dark>click</v-chip>
                            </v-col>
                          </v-row>
                          <v-card-subtitle class="py-0">{{
                            card2.gu
                          }}</v-card-subtitle>
                          <v-list-item>
                            <v-list-item-content class="pt-3 pb-1">
                              <v-list-item-title class="mytitle">{{
                                card2.date | ChangeDate
                              }}</v-list-item-title>
                              <v-list-item-subtitle class="mysubtitle">
                                매치 경기 시간:
                                {{ card2.fixed_time | ChangeTime }}시
                              </v-list-item-subtitle>
                            </v-list-item-content>
                          </v-list-item>
                        </v-img>
                      </v-card>

                      <v-card v-else-if="card2.status == 5" class="ml-1 mr-1">
                        <v-img class="semi_card_image" :src="card2.matchSrc">
                          <v-card-title>{{ card2.sports }}</v-card-title>
                          <v-card-subtitle class="py-0">{{
                            card2.gu
                          }}</v-card-subtitle>
                          <v-list-item>
                            <v-list-item-content class="pt-0 my-0 pb-1">
                              <v-list-item-title class="mytitle">{{
                                card2.date | ChangeDate
                              }}</v-list-item-title>
                              <v-list-item-subtitle class="mysubtitle">
                                매치 경기 시간:
                                {{ card2.fixed_time | ChangeTime }}시
                              </v-list-item-subtitle>
                              <p
                                v-if="card2.result == 1"
                                style="margin: 12px 0px"
                              >
                                결과: 승리
                              </p>
                              <p v-else style="margin: 12px 0px">결과: 패배</p>
                            </v-list-item-content>
                          </v-list-item>
                        </v-img>
                      </v-card>
                    </v-slide-item>
                  </v-slide-group>
                </v-expansion-panel-content>
              </v-expansion-panel>
            </v-expansion-panels>
          </v-row>
        </div>
      </v-container>
    </v-card>
  </div>
</template>

<script>
import http from "@/util/http-common";
import { mapState } from "vuex";

export default {
  name: "Profile",
  components: {},
  data() {
    return {
      type: "month",
      mode: "stack",
      weekday: [0, 1, 2, 3, 4, 5, 6],
      weekdays: [{ text: "Mon - Sun", value: [1, 2, 3, 4, 5, 6, 0] }],
      value: "",
      events: [],
      colors: [
        "#FF1E00",
        "#CC1800",
        "#991200",
        "#660C00",
        "#330600",
        "#290702",
      ],
      matchSrc: [
        require("@/assets/images/sports/futsal.png"),
        require("@/assets/images/sports/basketball.png"),
        require("@/assets/images/sports/pool.png"),
        require("@/assets/images/sports/tennis.png"),
        require("@/assets/images/sports/bowling.png"),
      ],

      confirmedMatch: {
        title: "확정된 경기",
        cards2: [],
      },

      userProfile: sessionStorage.getItem("userProfile")
        ? JSON.parse(sessionStorage.getItem("userProfile"))
        : [],
      cards1: [
        {
          title: "끝내주는 상대를 찾는 중",
          flex: 12,
          cards2: [],
        },
        {
          title: "조율중인 경기",
          flex: 12,
          cards2: [],
        },
        // {
        //   title: "대기중인 경기",
        //   flex: 12,
        //   cards2: [],
        // },
        {
          title: "진행중인 경기",
          flex: 12,
          cards2: [],
        },
        {
          title: "완료된 경기",
          flex: 12,
          cards2: [],
        },
      ],
      room_master: null,
    };
  },
  created() {
    this.getEvents();
  },
  computed: {
    ...mapState(["token"]),
  },
  methods: {
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
    getEvents({ start, end }) {
      const events = [];
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
            const temp_sports = "";
            const match_src = "";
            if (i.sports_name == "futsal") {
              temp_sports = "풋살";
              match_src = self.matchSrc[0];
            } else if (i.sports_name == "basket_ball") {
              temp_sports = "농구";
              match_src = self.matchSrc[1];
            } else if (i.sports_name == "pool") {
              temp_sports = "당구";
              match_src = self.matchSrc[2];
            } else if (i.sports_name == "tennis") {
              temp_sports = "테니스";
              match_src = self.matchSrc[3];
            } else {
              temp_sports = "볼링";
              match_src = self.matchSrc[4];
            }

            const temp_gu = i.gu.split("_");

            if (i.status == 1) {
              self.cards1[0].cards2.push({
                sports: temp_sports,
                date: i.date,
                start_time: i.start_time,
                end_time: i.end_time,
                gu: temp_gu[0] + " " + temp_gu[1],
                status: i.status,
                matchSrc: match_src,
              });
            } else if (i.status == 2) {
              self.cards1[1].cards2.push({
                sports: temp_sports,
                date: i.date,
                match_pk: i.matching_pk,
                match_start: i.match_start,
                match_end: i.match_end,
                gu: temp_gu[0] + " " + temp_gu[1],
                status: i.status,
                matchSrc: match_src,
              });
            } else if (i.status == 3) {
              self.confirmedMatch.cards2.push({
                sports: temp_sports,
                date: i.date,
                fixed_time: i.fixed_time,
                gu: temp_gu[0] + " " + temp_gu[1],
                status: i.status,
                matchSrc: match_src,
              });
            } else if (i.status == 4) {
              self.cards1[2].cards2.push({
                sports: temp_sports,
                date: i.date,
                fixed_time: i.fixed_time,
                match_pk: i.matching_pk,
                gu: temp_gu[0] + " " + temp_gu[1],
                status: i.status,
                matchSrc: match_src,
              });
            } else {
              self.cards1[3].cards2.push({
                sports: temp_sports,
                date: i.date,
                fixed_time: i.fixed_time,
                result: i.result,
                gu: temp_gu[0] + " " + temp_gu[1],
                status: i.status,
                matchSrc: match_src,
              });
            }
          }

          for (let i = 0; i < self.cards1.length; i++) {
            const cards2_test = self.cards1[i];
            for (let j = 0; j < cards2_test["cards2"].length; j++) {
              self.events.push({
                name: cards2_test["cards2"][j]["sports"],
                start: cards2_test["cards2"][j]["date"],
                end: cards2_test["cards2"][j]["date"],
                color: self.colors[cards2_test["cards2"][j]["status"]],
              });
            }
          }
        })
        .catch(function (err) {
          alert(err);
        });
    },
    getEventColor(event) {
      return event.color;
    },
    rnd(a, b) {
      return Math.floor((b - a + 1) * Math.random()) + a;
    },
  },
  filters: {
    ChangeTime(value) {
      return value.split(":")[0];
    },
    ChangeDate(value) {
      var RawDate = value.split("-");
      var newDate =
        RawDate[0] + "년" + " " + RawDate[1] + "월" + " " + RawDate[2] + "일";
      return newDate;
    },
  },
};
</script>

<style scoped>
.card_image {
  /* margin-top: 1vh; */
  /* margin-left: 5vw; */
  height: 26vh;
  width: 26vh;
  border-radius: 10px;
}

.accordion_card {
  border-radius: 0px;
  font-weight: bold;
  padding: 0;
}

.semi_card_image {
  /* margin-top: 1vh; */
  /* margin-left: 5vw; */
  height: 26vh;
  width: 40vh;
  border-radius: 10px;
}

.card_title {
  padding-left: 14px;
  padding-top: 14px;
  padding-bottom: 4px;
}

.page_title {
  padding-left: 6px;
  padding-right: 10px;
  padding-top: 8px;
  margin-bottom: 0px;
  /* margin-right: 2px; */
  font-size: 23px;
}

.month_title {
  font-size: 18px;
  line-height: 8.5vh;
  font-weight: bold;
  color: #290702;
}

.mytitle {
  font-size: 17px;
  color: #000000;
  /* font-weight: bold; */
  line-height: 17px;
  margin-top: 20px;
}

.mysubtitle {
  font-size: 14px;
  color: rgb(255, 255, 255);
}

.mycard {
  opacity: 0.3;
}

.noItem {
  opacity: 0.98;
}

.noMatch {
  text-align: center;
  position: relative;
  top: 10vh;
  height: 24vh;
  color: #acacac;
  font-weight: 400;
}
</style>