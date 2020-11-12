<template>
  <v-card class="mx-auto" max-width="720">
    <h1>조율하는 방</h1>
    <p>{{ match_id }}번 경기</p>
    <p>방장: {{ room_master }}</p>
    <p>중앙위치: {{ center_lat }}, {{ center_lng }}</p>
    <p>내 번호: {{ userProfile.id }}</p>
    <p>{{ users }}</p>
    <p>유저들: {{ users_pk }}</p>

    <v-row style="margin: 10px">
      <v-checkbox
        v-for="(user, key) in users"
        :key="user.username"
        v-model="teamA"
        :label="user.username"
        :value="key"
      ></v-checkbox>
    </v-row>
    <p>{{ teamA }}</p>
    <p>{{ teamB }}</p>
    <p>{{ fixed_users }}</p>

    <v-row class="mx-1">
      <v-col cols="12" class="py-0">
        <v-slider
          v-model="ex3.val"
          :label="ex3.label"
          :thumb-color="ex3.color"
          :min="6"
          :max="22"
          step="1"
          thumb-label="always"
        ></v-slider>
      </v-col>
    </v-row>
    <p>{{ this.ex3.val }}</p>

    <v-btn v-if="userProfile.id == room_master" @click="inputAfterMatch">
      확정
    </v-btn>
  </v-card>
</template>

<script>
import http from "@/util/http-common";
import { mapState } from "vuex";

export default {
  name: "MatchRoom",
  components: {},
  data() {
    return {
      userProfile: sessionStorage.getItem("userProfile")
        ? JSON.parse(sessionStorage.getItem("userProfile"))
        : [],
      match_id: this.$route.query.match_id,
      room_master: null,
      center_lat: "",
      center_lng: "",
      users_pk: [],

      fixed_lat: "37.477107637586194",
      fixed_lng: "126.96346058714246",
      ex3: { label: "확정시간", val: 50, color: "red" },
      teamA: [],
      teamB: [],
      fixed_users: {},
    };
  },
  computed: {
    ...mapState(["token"]),
  },
  created() {
    this.getRoomData(this.match_id);
  },
  methods: {
    getRoomData(match_id) {
      console.log(match_id);
      console.log(this.token);
      http
        .post(
          "/match/match-room/",
          { match_pk: match_id },
          {
            headers: {
              Authorization: "JWT " + this.token,
            },
          }
        )
        .then((res) => {
          console.log(res);
          this.room_master = Object.keys(res.data.data[0].users)[0];
          this.center_lat = res.data.data[0].match_lat;
          this.center_lng = res.data.data[0].match_lng;
          this.users = res.data.data[0].users;
          this.users_pk = Object.keys(res.data.data[0].users);
        })
        .catch((err) => {
          console.log(err);
        });
    },
    inputAfterMatch() {
      if (this.teamA.length == this.users_pk.length / 2) {
        http
          .post(
            "/match/am/",
            {
              match_pk: this.match_id,
              // fixed_time: this.ex3.val,
              fixed_time: "09:00:00",
              users: this.fixed_users,
              fixed_lat: this.fixed_lat,
              fixed_lng: this.fixed_lng,
            },
            {
              headers: {
                Authorization: "JWT " + this.token,
              },
            }
          )
          .then((res) => {
            console.log(res);
          })
          .catch((err) => {
            console.log(err);
          });
      } else {
        alert("각 팀의 인원 수가 같아야 합니다.");
      }
    },
  },
  watch: {
    teamA(values) {
      if (values.length == this.users_pk.length / 2) {
        this.teamB = this.users_pk.filter((item) => !values.includes(item));
      } else {
        this.teamB = [];
      }
      console.log(this.users_pk);
      for (const user_pk of this.users_pk) {
        console.log(user_pk);
        console.log(values);
        if (values.includes(user_pk)) {
          this.fixed_users[user_pk] = { team: 0 };
        } else {
          this.fixed_users[user_pk] = { team: 1 };
        }
      }
    },
  },
};
</script>

<style>
</style>