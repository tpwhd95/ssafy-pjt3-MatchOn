<template>
  <v-card class="mx-auto" max-width="720">
    <h1>경기결과 입력</h1>
    <p>경기 번호: {{ match_id }}</p>
    <p>종목: {{ sports }}</p>
    <p>날짜: {{ date }}</p>
    <p>시간: {{ time | ChangeTime }}시</p>
    <v-btn @click="inputResult(true)">승리</v-btn>
    <v-btn @click="inputResult(false)">패배</v-btn>

    <v-snackbar v-model="alert_collide">
      이미 결과를 입력하셨습니다. 상대방이 결과를 입력할 때까지 기다려주세요.
      <template v-slot:action="{ attrs }">
        <v-btn color="pink" text v-bind="attrs" @click="alert_collide = false">
          닫기
        </v-btn>
      </template>
    </v-snackbar>
  </v-card>
</template>

<script>
import http from "@/util/http-common";
import { mapState } from "vuex";
import fb from "@/firebase/init";

export default {
  name: "ResultRoom",
  components: {},
  data() {
    return {
      match_id: this.$route.query.match_id,
      sports: this.$route.query.sports,
      date: this.$route.query.date,
      time: this.$route.query.time,
      user_profile: JSON.parse(sessionStorage.getItem("userProfile")),
      room_results_ref: null,
      room_users_ref: null,
      my_team: "0",
      alert_collide: false,
    };
  },
  computed: {
    ...mapState(["token"]),
  },
  methods: {
    inputResult(result) {
      // 경기 결과 데이터 입력
      console.log(" 경기 결과 데이터 입력 시작");

      const my_status = result ? 2 : 1;
      // 상대편 상태를 가져옴
      let opposit_status = 0;
      let isAlready = false;
      this.room_results_ref
        .get()
        .then((querySnapshot) => {
          querySnapshot.forEach((doc) => {
            if (doc.id != this.my_team)
              opposit_status = doc.data().match_result;
            else if (doc.data().match_result != 0) {
              console.log("이미 입력 마침");
              this.alert_collide = true;
              isAlready = true;
            }
          });
        })
        .then(() => {
          if (isAlready) return;

          // 상대편이 0이 아닐 경우
          if (opposit_status != 0) {
            console.log(" 상대편이 입력을 마친 상태");
            // 내 값과 상대방의 값이 같으면 충돌
            if (my_status == opposit_status) {
              console.log("충돌 남");

              this.$router.push("/resultfalse");
              this.room_results_ref.get().then((querySnapshot) => {
                querySnapshot.forEach((doc) => {
                  doc.ref.set({
                    match_result: 0,
                  });
                });
              });
              return;
            }
          }

          console.log("경기 결과  입력");
          this.room_results_ref.doc(this.my_team).set({
            match_result: my_status,
          });
        });
    },
    inputResultWin() {
      http
        .post(
          "/match/result/",
          {
            match_pk: this.match_id,
            result: "true",
          },
          {
            headers: {
              Authorization: "JWT " + this.token,
            },
          }
        )
        .then((res) => {
          console.log(res);
          if (res.data.result == "ready") {
            console.log("ready");
          } else if (res.data.result == "error") {
            console.log("error");
            this.$router.push("/resulterror");
          } else if (res.data.result == "false") {
            console.log("false");
            this.$router.push("/resultfalse");
          } else if (res.data.result == "true") {
            console.log("true");
            this.$router.push("/resulttrue");
          }
        })
        .catch((err) => {
          console.log(err);
        });
    },
    inputResultLose() {
      http
        .post(
          "/match/result/",
          {
            match_pk: this.match_id,
            result: "false",
          },
          {
            headers: {
              Authorization: "JWT " + this.token,
            },
          }
        )
        .then((res) => {
          console.log(res);
          if (res.data.result == "ready") {
            console.log("ready");
            this.$router.push("/resultready");
          } else if (res.data.result == "error") {
            console.log("error");
            this.$router.push("/resulterror");
          } else if (res.data.result == "false") {
            console.log("false");
            this.$router.push("/resultfalse");
          } else if (res.data.result == "true") {
            console.log("true");
            this.$router.push("/resulttrue");
          }
        })
        .catch((err) => {
          console.log(err);
        });
    },
  },
  filters: {
    ChangeTime(value) {
      return value.split(":")[0];
    },
  },
  beforeMount() {
    this.room_results_ref = fb.collection(
      "room_results" + String(this.match_id)
    );
    this.room_users_ref = fb.collection("room_users" + String(this.match_id));
  },
  mounted() {
    this.room_results_ref.onSnapshot((snapshot) => {
      snapshot.docChanges().forEach((change) => {
        if (change.type === "modified") {
          console.log("변경 발생");
          this.room_results_ref.get().then((querySnapshot) => {
            let my_status = 0;
            let opposit_status = 0;
            querySnapshot.forEach((doc) => {
              if (doc.id == this.my_team) {
                my_status = doc.data().match_result;
              } else {
                opposit_status = doc.data().match_result;
              }
            });

            // 내 상태가 0
            if (my_status == 0) {
              // 모달 클로즈
              console.log("모달 클로즈");
            }
            // 내 상태가 0이 아닌데 상대가 0이면
            else if (my_status != 0 && opposit_status == 0) {
              // 대기 중 모달 출력
              console.log("대기 중");
              this.$router.push("/resultready");
            }
            // 내 상태가 0이 아니고 상대도 0이 아니면
            else if (my_status != 0 && opposit_status != 0) {
              // 경기 종료 로직
              console.log("경기 종료");
              this.$router.push("/resulttrue");
            }
          });
        }
      });
    });

    this.room_users_ref.get().then((querySnapshot) => {
      querySnapshot.forEach((doc) => {
        if (doc.data().user_id == this.user_profile.id) {
          this.my_team = doc.data().user.team ? "1" : "0";
          console.log(this.my_team);
        }
      });
    });
  },
};
</script>

<style>
</style>