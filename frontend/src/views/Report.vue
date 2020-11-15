<template>
  <div>
    <v-card class="mx-auto" max-width="720">
      <v-container fluid>
        <h2>{{ userProfile.username }}님의 전적</h2>
        <v-row>
          <v-col v-for="card1 in cards1" :key="card1.title" :cols="card1.flex">
            <v-card style="padding: 16px">
              <h3>{{ card1.title }}</h3>
              <p>{{ card1.total }}</p>
              <p>{{ card1.rate }}</p>
              <p>{{ card1.win }}</p>
              <p>{{ card1.lose }}</p>
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
  name: "Report",
  components: {},
  data() {
    return {
      userProfile: sessionStorage.getItem("userProfile")
        ? JSON.parse(sessionStorage.getItem("userProfile"))
        : [],
      cards1: [
        {
          title: "풋살",
          flex: 12,
          total: "",
          win: "",
          lose: "",
          rate: "",
        },
        {
          title: "농구",
          flex: 12,
          total: "",
          win: "",
          lose: "",
          rate: "",
        },
        {
          title: "테니스",
          flex: 12,
          total: "",
          win: "",
          lose: "",
          rate: "",
        },
        {
          title: "당구",
          flex: 12,
          total: "",
          win: "",
          lose: "",
          rate: "",
        },
        {
          title: "볼링",
          flex: 12,
          total: "",
          win: "",
          lose: "",
          rate: "",
        },
      ],
    };
  },
  computed: {
    ...mapState(["token"]),
  },
  methods: {
    getReport() {
      http
        .get("/match/report", {
          headers: {
            Authorization: "JWT " + this.token,
          },
        })
        .then((res) => {
          const dict = {
            futsal: 0,
            basket_ball: 1,
            tennis: 2,
            pool: 3,
            bowling: 4,
          };
          console.log(res);
          for (const key in res.data) {
            this.cards1[dict[key]].total = res.data[key].total;
            this.cards1[dict[key]].win = res.data[key].win;
            this.cards1[dict[key]].lose = res.data[key].lose;
            this.cards1[dict[key]].data = res.data[key].data;
          }

          //   this.cards1[0].total = res.data["futsal"].total;
          //   this.cards1[0].win = res.data["futsal"].win;
          //   this.cards1[0].lose = res.data["futsal"].lose;
          //   this.cards1[0].rate = res.data["futsal"].rate;

          //   this.cards1[1].total = res.data["basket_ball"].total;
          //   this.cards1[1].win = res.data["basket_ball"].win;
          //   this.cards1[1].lose = res.data["basket_ball"].lose;
          //   this.cards1[1].rate = res.data["basket_ball"].rate;

          //   this.cards1[2].total = res.data["tennis"].total;
          //   this.cards1[2].win = res.data["tennis"].win;
          //   this.cards1[2].lose = res.data["tennis"].lose;
          //   this.cards1[2].rate = res.data["tennis"].rate;

          //   this.cards1[3].total = res.data["pool"].total;
          //   this.cards1[3].win = res.data["pool"].win;
          //   this.cards1[3].lose = res.data["pool"].lose;
          //   this.cards1[3].rate = res.data["pool"].rate;

          //   this.cards1[4].total = res.data["bowling"].total;
          //   this.cards1[4].win = res.data["bowling"].win;
          //   this.cards1[4].lose = res.data["bowling"].lose;
          //   this.cards1[4].rate = res.data["bowling"].rate;
        })
        .catch((error) => {
          console.log(error);
        });
    },
  },
};
</script>

<style>
</style>