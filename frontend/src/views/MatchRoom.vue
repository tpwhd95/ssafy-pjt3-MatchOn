<template>
  <v-card class="mx-auto" max-width="720">
    <h1>조율하는 방</h1>
    <p>{{ match_id }}번 경기</p>
    <p>방장: {{ room_master }}</p>
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
      match_id: this.$route.query.match_id,
      room_master: null,
      center_lat: "",
      center_lng: "",
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
          console.log(this.room_master);
          this.center_lat = res.data.data[0].match_lat;
          this.center_lng = res.data.data[0].match_lng;
        })
        .catch((err) => {
          console.log(err);
        });
    },
  },
};
</script>

<style>
</style>