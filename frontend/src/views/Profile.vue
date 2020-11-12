<template>
  <div>
    <v-card class="mx-auto" max-width="720">
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
                    v-if="card1.title == '매칭중인 경기'"
                    style="padding: 8px"
                  >
                    <p style="margin: 12px 0px">종목: {{ card2.sports }}</p>
                    <p style="margin: 12px 0px">날짜: {{ card2.date }}</p>
                    <p style="margin: 12px 0px">
                      시간: {{ card2.start_time | ChangeTime }}시 ~
                      {{ card2.end_time | ChangeTime }}시
                    </p>
                  </v-card>

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

                  <v-card
                    v-if="card1.title == '완료된 경기'"
                    style="padding: 8px"
                  >
                    <p style="margin: 12px 0px">종목: {{ card2.sports }}</p>
                    <p style="margin: 12px 0px">날짜: {{ card2.date }}</p>
                    <p style="margin: 12px 0px">
                      시간: {{ card2.fixed_time | ChangeTime }}시
                    </p>
                    <p v-if="card2.result == 1" style="margin: 12px 0px">
                      결과: 승리
                    </p>
                    <p v-else style="margin: 12px 0px">결과: 패배</p>
                  </v-card>
                </v-col>
              </v-row>
            </v-card>
          </v-col>
        </v-row>
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
      userProfile: sessionStorage.getItem("userProfile")
        ? JSON.parse(sessionStorage.getItem("userProfile"))
        : [],
      cards1: [
        {
          title: "매칭중인 경기",
          flex: 12,
          cards2: [],
        },
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
        {
          title: "완료된 경기",
          flex: 12,
          cards2: [],
        },
      ],
    };
  },
  created() {
    this.getMatchInfo();
  },
  computed: {
    ...mapState(["token"]),
  },
  methods: {
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
            if (i.status == 1) {
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
              if (i.sports_name == "bowl") {
                temp_sports = "볼링";
              }
              self.cards1[0].cards2.push({
                sports: temp_sports,
                date: i.date,
                flex: 12,
                start_time: i.start_time,
                end_time: i.end_time,
              });
            }
            if (i.status == 2) {
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
              if (i.sports_name == "bowl") {
                temp_sports = "볼링";
              }
              self.cards1[1].cards2.push({
                sports: temp_sports,
                date: i.date,
                flex: 12,
                match_pk: i.matching_pk,
                match_start: i.match_start,
                match_end: i.match_end,
              });
            }
            if (i.status == 3) {
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
              if (i.sports_name == "bowl") {
                temp_sports = "볼링";
              }
              self.cards1[2].cards2.push({
                sports: temp_sports,
                date: i.date,
                flex: 12,
                fixed_time: i.fixed_time,
              });
            }
            if (i.status == 4) {
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
              self.cards1[3].cards2.push({
                sports: temp_sports,
                date: i.date,
                flex: 12,
                fixed_time: i.fixed_time,
                match_pk: i.matching_pk,
              });
            }
            if (i.status == 5) {
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
              if (i.sports_name == "bowl") {
                temp_sports = "볼링";
              }
              self.cards1[4].cards2.push({
                sports: temp_sports,
                date: i.date,
                flex: 12,
                fixed_time: i.fixed_time,
                result: i.result,
              });
            }
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
        params: { match_id: match_id },
      });
    },
    getResultRoom(match_id, sports, date, time) {
      console.log(match_id);
      console.log(this.token);
      this.$router.push({
        name: "ResultRoom",
        params: { match_id: match_id, sports: sports, date: date, time: time },
      });
    },
  },
  filters: {
    ChangeTime(value) {
      return value.split(":")[0];
    },
  },
};
</script>

<style>
</style>