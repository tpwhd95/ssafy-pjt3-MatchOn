<template>
  <div>
    <v-card class="mx-auto" max-width="720">
      <v-container fluid>
        <h2>{{ userProfile.username }}님의 전적</h2>
        <v-row>
          <v-col v-for="card1 in cards1" :key="card1.title" :cols="card1.flex">
            <v-card
              style="padding: 16px"
              @click="reportDetail(card1.sports_id)"
            >
              <h3>{{ card1.title }}</h3>
              <p>{{ card1.total }}전</p>
              <p>{{ card1.win }}승</p>
              <p>{{ card1.lose }}패</p>
              <p>승률: {{ card1.rate }}%</p>
              <p>sports_id: {{ card1.sports_id }}</p>
            </v-card>
          </v-col>
        </v-row>
      </v-container>
    </v-card>
  </div>
</template>

<script>
import http from "@/util/http-common";
import { mapState, mapActions } from "vuex";

export default {
  name: "Report",
  components: {},
  data() {
    return {
      detailDatas: [],
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
          sports_id: "",
        },
        {
          title: "농구",
          flex: 12,
          total: "",
          win: "",
          lose: "",
          rate: "",
          sports_id: "",
        },
        {
          title: "테니스",
          flex: 12,
          total: "",
          win: "",
          lose: "",
          rate: "",
          sports_id: "",
        },
        {
          title: "당구",
          flex: 12,
          total: "",
          win: "",
          lose: "",
          rate: "",
          sports_id: "",
        },
        {
          title: "볼링",
          flex: 12,
          total: "",
          win: "",
          lose: "",
          rate: "",
          sports_id: "",
        },
      ],
    };
  },
  computed: {
    ...mapState(["reportlist"]),
  },
  created() {
    this.getReport();
  },
  methods: {
    ...mapActions(["getReport"]),
    reportDetail(sports_pk) {
      this.$emit("report-detail", sports_pk);
    },
  },
  watch: {
    reportlist(value) {
      console.log(value);
      const dict = {
        futsal: 0,
        basket_ball: 1,
        tennis: 2,
        pool: 3,
        bowling: 4,
      };
      for (const key in value) {
        this.cards1[dict[key]].total = value[key].total;
        this.cards1[dict[key]].win = value[key].win;
        this.cards1[dict[key]].lose = value[key].lose;
        this.cards1[dict[key]].rate = value[key].rate;
        this.cards1[dict[key]].sports_id = value[key].sports_id;
      }
    },
  },
};
</script>

<style>
</style>