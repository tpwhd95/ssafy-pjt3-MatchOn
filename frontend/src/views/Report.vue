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
              <h2>{{ card1.title }}</h2>
              <v-row>
                <v-col class="d-flex align-center">
                  <span style="margin-right: 5px">{{ card1.total }}전</span>
                  <span style="margin-right: 5px">{{ card1.win }}승</span>
                  <span style="margin-right: 5px">{{ card1.lose }}패</span>
                  <!-- <span>승률: {{ card1.rate }}%</span> -->
                  <!-- <p>sports_id: {{ card1.sports_id }}</p> -->
                </v-col>
                <v-col>
                  <v-progress-circular
                    :rotate="-90"
                    :size="100"
                    :width="15"
                    :value="card1.rate"
                    color="primary"
                  >
                    {{ card1.rate }}%
                  </v-progress-circular>
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