<template>
  <div>
    <v-card class="mx-auto" max-width="720">
      <v-card-title class="pb-0 mt-1 match_title">
        <div>
          <span class="ft-dh bold">{{ userProfile.username }}님의 전적</span>
          <!-- <span class="ft-dh span_title">종목을 </span>
          <span class="ft-dh onred bold">온 </span>
          <span class="ft-dh span_title">하세요!</span> -->
        </div>
      </v-card-title>

      <v-container fluid>
        <v-row>
          <v-col v-for="card1 in cards1" :key="card1.title">
            <v-card :elevation="7">
              <v-img :src="card1.src" height="150px">
                <div class="d-flex flex-no-wrap justify-space-between">
                  <div>
                    <v-card-title class="headline">{{
                      card1.title
                    }}</v-card-title>

                    <v-card-subtitle>
                      {{ card1.total }}전 {{ card1.win }}승 {{ card1.lose }}패
                    </v-card-subtitle>
                  </div>
                  <div class="mt-5 mr-5">
                    <v-progress-circular
                      :rotate="-90"
                      :size="100"
                      :width="15"
                      :value="card1.rate"
                      color="#0f4c81"
                    >
                      {{ card1.rate }}%
                    </v-progress-circular>
                  </div>
                </div>
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
          src: require("@/assets/images/sports/futsal.png"),
        },
        {
          title: "농구",
          flex: 12,
          total: "",
          win: "",
          lose: "",
          rate: "",
          sports_id: "",
          src: require("@/assets/images/sports/basketball.png"),
        },
        {
          title: "테니스",
          flex: 12,
          total: "",
          win: "",
          lose: "",
          rate: "",
          sports_id: "",
          src: require("@/assets/images/sports/tennis.png"),
        },
        {
          title: "당구",
          flex: 12,
          total: "",
          win: "",
          lose: "",
          rate: "",
          sports_id: "",
          src: require("@/assets/images/sports/pool.png"),
        },
        {
          title: "볼링",
          flex: 12,
          total: "",
          win: "",
          lose: "",
          rate: "",
          sports_id: "",
          src: require("@/assets/images/sports/bowling.png"),
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
.match_title {
  font-size: 23px;
  padding-left: 19px;
  padding-top: 18px;
  text-align: center;
}

.card_title {
  font-size: 35px;
  line-height: 23vh;
  font-weight: 400;
  /* opacity: 0.8; */
  color: black;
  /* align-items: center; */
}

.card_design {
  text-align: center;
}
</style>