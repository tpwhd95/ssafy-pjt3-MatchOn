<template>
  <div class="h-100">
    <div v-if="!this.cards1[0].cards2.length" class="h-100">
      <v-container
        class="h-100 mx-auto d-flex justify-center align-center pb-15 bg-brown"
        max-width="720"
      >
        <div class="text-center">
          <h2 class="main-text ft-dh mb-7">
            온라인 스포츠 <span class="ft-dh onred bold"> 매칭 </span>서비스
          </h2>
          <img
            src="@/assets/images/logos/full_logo_black.png"
            alt="match-on-logo"
            style="height: 150px"
            class="mb-7"
          />
          <h3 v-if="!this.isLoggedIn" class="main-text">
            서비스 사용을 위해 로그인해주세요
          </h3>
          <div>
            <v-btn
              v-if="this.isLoggedIn"
              to="/match"
              color="rgb(189, 22, 44)"
              dark
            >
              한 판 붙자!
            </v-btn>
          </div>
        </div>
      </v-container>
    </div>
    <div v-else>
      <div v-for="card1 in cards1" :key="card1.title">
        <h1 class="ml-4 my-4">{{ card1.title }}</h1>
        <h3 class="ml-4 my-4">경기가 끝나면 결과를 입력해주세요.</h3>
        <v-card
          v-for="card2 in card1.cards2"
          :key="card2"
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
            <v-card-title class="font-weight-black">{{
              card2.sports
            }}</v-card-title>
            <v-card-subtitle>{{ card2.gu }}</v-card-subtitle>
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
      </div>
    </div>
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
      cards1: [
        {
          title: "진행중인 경기",
          flex: 12,
          cards2: [],
        },
      ],
      matchSrc: [
        require("@/assets/images/sports/futsal.png"),
        require("@/assets/images/sports/basketball.png"),
        require("@/assets/images/sports/pool.png"),
        require("@/assets/images/sports/tennis.png"),
        require("@/assets/images/sports/bowling.png"),
      ],
    };
  },
  created() {
    if (this.isLoggedIn) {
      this.getEvents();
    }
  },
  methods: {
    getEvents() {
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

            if (i.status == 4) {
              self.cards1[0].cards2.push({
                sports: temp_sports,
                date: i.date,
                fixed_time: i.fixed_time,
                match_pk: i.matching_pk,
                gu: temp_gu[0] + " " + temp_gu[1],
                status: i.status,
                matchSrc: match_src,
              });
            }
          }
        })
        .catch(function (err) {
          alert(err);
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
  },
  computed: {
    ...mapGetters(["isLoggedIn"]),
    ...mapState(["token"]),
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
.h-100 {
  height: 100%;
}

.bg-brown {
  background-color: rgba(32, 32, 32, 0.925);
}

.main-text {
  color: rgba(255, 255, 255, 0.863);
}

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
  width: 50vh;
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
}

.mysubtitle {
  font-size: 15px;
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