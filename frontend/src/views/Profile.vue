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
              self.cards1[0].cards2.push({
                sports: i.sports_name,
                date: i.date,
                flex: 12,
              });
            }
            if (i.status == 2) {
              self.cards1[1].cards2.push({
                sports: i.sports_name,
                date: i.date,
                flex: 12,
              });
            }
            if (i.status == 3) {
              self.cards1[2].cards2.push({
                sports: i.sports_name,
                date: i.date,
                flex: 12,
              });
            }
            if (i.status == 4) {
              self.cards1[3].cards2.push({
                sports: i.sports_name,
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