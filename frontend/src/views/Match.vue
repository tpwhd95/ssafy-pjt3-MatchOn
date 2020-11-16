<template>
  <div>
    <!-- 비로그인 디비전 -->
    <v-main v-if="!this.isLoggedIn" class="mx-auto" max-width="720">
      <v-container fluid>
        <div class="text-center d-flex align-center">
          <img src="@/assets/images/logos/logo.png" style="width: 100%" />
        </div>
      </v-container>
    </v-main>

    <!-- 매칭 신청 -->
    <v-card v-else class="mx-auto card_design" max-width="720">
      <v-card-title class="match_title pb-0 mt-1">
        <div>
          <span class="ft-dh bold">매치 </span>
          <span class="ft-dh span_title">종목을 </span>
          <span class="ft-dh onred bold">온 </span>
          <span class="ft-dh span_title">하세요!</span>
        </div>
      </v-card-title>

      <v-container fluid>
        <v-row>
          <v-col
            v-for="card in cards"
            :key="card.title"
            :sportsName="card.title"
            class="pb-0"
          >
            <v-card :elevation="5" class="card_design">
              <v-img
                :src="card.src"
                class="white--text"
                gradient="to bottom, rgba(0,0,0,.05), rgba(0,0,0,.6)"
                height="150px"
                @click="matching(card.title, card.title2)"
                style="cursor: pointer"
              >
              <span class="card_title ft-dh">{{ card.title2 }}</span>
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
    };
  },
  methods: {
    matching(sportsName, sportsNameKR) {
      this.$router.push({
        name: "About",
        query: { sports: sportsName, sportsKR: sportsNameKR },
      });
    },
  },
  computed: {
    ...mapGetters(["isLoggedIn"]),
    ...mapState(["token"]),
  },
};
</script>

<style scoped>
.match_title {
  font-size: 28px;
  text-align: center;
}

.match_image {
  height: 26vh;
  width: 26vh;
  border-radius: 10px;
}

.card_title {
  font-size: 35px;
  line-height: 23vh;
  font-weight: 400;
  opacity: 0.8;
  color: #ffffff;
  /* align-items: center; */
}

/* .card_design {
  text-align: center;
} */

.span_title {
  color: rgb(58, 58, 58);
  opacity: 0.85;
}
</style>
