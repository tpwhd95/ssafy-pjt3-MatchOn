<template>
  <div>
    <v-card class="mx-auto" max-width="720">
      <v-container fluid>
        <h2>{{ userProfile.username }}님의 경기 정보</h2>
        <v-row>
          <v-col v-for="card1 in cards1" :key="card1.title" :cols="card1.flex">
            <v-card>
              <h3>{{ card1.title }}</h3>
              <v-row>
                <v-col
                  v-for="card2 in card1.cards2"
                  :key="card2.sports"
                  :cols="card2.flex"
                >
                  <v-card>
                    <p>{{ card2.sports }}</p>
                    <p>{{ card2.date }}</p>
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
      cards2_1: [],
      cards2_2: [],
      cards2_3: [],
      cards2_4: [],

      cards1: [
        {
          title: "매칭중인 경기",
          flex: 12,
          cards2: this.cards2_1,
        },
        {
          title: "조율중인 경기",
          flex: 12,
          cards2: this.cards2_2,
        },
        {
          title: "대기중인 경기",
          flex: 12,
          cards2: this.cards2_3,
        },
        {
          title: "완료된 경기",
          flex: 12,
          cards2: this.cards2_4,
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
      const self = this;
      http
        .get("/auth/match-info/", {
          headers: {
            Authorization: "JWT " + this.token,
          },
        })
        .then(function (res) {
          if (res.status == 1) {
            self.cards2_1 = [];
            for (let i of res.data) {
              self.cards2_1.push({
                sports: i.sports,
                date: i.date,
                flex: 12,
              });
            }
          }
          if (res.status == 2) {
            self.cards2_2 = [];
            for (let i of res.data) {
              self.cards2_2.push({
                sports: i.sports,
                date: i.date,
                flex: 12,
              });
            }
          }
          if (res.status == 3) {
            self.cards2_3 = [];
            for (let i of res.data) {
              self.cards2_3.push({
                sports: i.sports,
                date: i.date,
                flex: 12,
              });
            }
          }
          if (res.status == 4) {
            self.cards2_4 = [];
            for (let i of res.data) {
              self.cards2_4.push({
                sports: i.sports,
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