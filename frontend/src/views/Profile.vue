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
                  <v-card style="padding: 8px">
                    <p style="margin: 12px 0px">종목: {{ card2.sports }}</p>
                    <p style="margin: 12px 0px">날짜: {{ card2.date }}</p>
                    <p style="margin: 12px 0px">
                      시간: {{ card2.start_time }} ~ {{ card2.end_time }}
                    </p>
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
              if (i.sports_name == "bowl") {
                temp_sports = "볼링";
              }
              self.cards1[3].cards2.push({
                sports: temp_sports,
                date: i.date,
                flex: 12,
              });
            }
          }
        })
        .catch(function (err) {
          alert(err);
        });
    },
  },
};
</script>

<style>
</style>