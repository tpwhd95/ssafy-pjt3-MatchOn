<template>
  <v-card class="mx-auto text-center" max-width="720">
    <h1 class="ft-dh text-center">
      <span class="ft-dh">경기결과</span><span class="ft-dh onred">입력</span>
    </h1>
    <div class="mx-2 mt-10 mb-10">
      <strong>{{ date | changeDate }} </strong>
      <span
        ><strong>{{ time | ChangeTime }}시</strong>에 플레이한
      </span>
      <p>
        <strong>{{ sports }}</strong> 경기 결과를 입력해주세요.
      </p>
    </div>

    <!-- <div class="d-flex justify-space-around mt-16"> -->

    <v-btn
      style="width: 80%; height: 30%; font-size: 3rem"
      color="blue accent-4"
      dark
      @click="inputResult(true)"
      >승리</v-btn
    >
    <br />
    <br />
    <v-btn
      style="width: 80%; height: 30%; font-size: 3rem"
      color="red accent-4"
      dark
      @click="inputResult(false)"
      >패배</v-btn
    >

    <!-- </div> -->

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
              this.room_results_ref.doc(this.my_team).set({
                match_result: my_status,
              });
              console.log("충돌 남");

              this.room_results_ref
                .get()
                .then((querySnapshot) => {
                  querySnapshot.forEach((doc) => {
                    doc.ref.set({
                      match_result: 0,
                    });
                  });
                })
                .then(() => {
                  this.$router.push("/resultfalse");
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
  },
  filters: {
    ChangeTime(value) {
      return value.split(":")[0];
    },
    changeDate(value) {
      const year = value.split("-")[0];
      const month = value.split("-")[1];
      const date = value.split("-")[2];
      const answer = year + "년 " + month + "월 " + date + "일";
      return answer;
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
            if (my_status == 0 && opposit_status == 0) {
              // 모달 클로즈
              this.$router.push("/resultfalse");
            } else if (my_status == 0) {
              console.log("나 상태 0");
            }
            // 내 상태가 0이 아닌데 상대가 0이면
            else if (my_status != 0 && opposit_status == 0) {
              // 대기 중 모달 출력
              console.log("대기 중");
              this.$router.push("/resultready");
            }
            // 내 상태가 0이 아니고 상대도 0이 아니고 결과값이 같으면
            else if (
              my_status != 0 &&
              opposit_status != 0 &&
              my_status == opposit_status
            ) {
              // 충돌 로직
              console.log("충돌");
              this.$router.push("/resultfalse");
            }
            // 내 상태가 0이 아니고 상대도 0이 아니고 결과값이 다르면
            else if (
              my_status != 0 &&
              opposit_status != 0 &&
              my_status != opposit_status
            ) {
              // 경기 종료 로직
              console.log("경기 종료");
              this.$router.push("/resulttrue");
              if (my_status == 1) {
                my_status = "false";
                console.log("나는 졌다", this.match_id, my_status);
                http
                  .post(
                    "/match/result/",
                    {
                      match_pk: this.match_id,
                      result: my_status,
                    },
                    {
                      headers: {
                        Authorization: "JWT " + this.token,
                      },
                    }
                  )
                  .then((res) => {
                    console.log("경기 결과 입력 완료");
                  })
                  .catch((err) => {
                    console.log(err);
                  });
              } else if (my_status == 2) {
                my_status = "true";
                console.log("나는 이겼다", this.match_id, my_status);
                http
                  .post(
                    "/match/result/",
                    {
                      match_pk: this.match_id,
                      result: my_status,
                    },
                    {
                      headers: {
                        Authorization: "JWT " + this.token,
                      },
                    }
                  )
                  .then((res) => {
                    console.log("경기 결과 입력 완료");
                  })
                  .catch((err) => {
                    console.log(err);
                  });
              }
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