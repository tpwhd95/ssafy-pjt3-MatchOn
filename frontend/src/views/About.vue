<template>
  <v-form v-model="valid">
    <v-container>
      <v-row>
        <v-col cols="1">
          <v-text-field
            v-model="sportsName"
            label="종목"
            readonly
          ></v-text-field>
        </v-col>

        <v-col cols="2">
          <v-menu
            v-model="menu1"
            :close-on-content-click="false"
            :nudge-right="0"
            transition="scale-transition"
            offset-y
            min-width="290px"
          >
            <template v-slot:activator="{ on, attrs }">
              <v-text-field
                v-model="date1"
                label="날짜"
                readonly
                v-bind="attrs"
                v-on="on"
              ></v-text-field>
            </template>
            <v-date-picker
              v-model="date1"
              @input="menu1 = false"
              :min="today"
            ></v-date-picker>
          </v-menu>
        </v-col>

        <v-col cols="8">
          <v-range-slider
            v-model="time"
            :tick-labels="ticksLabels"
            :max="16"
            step="1"
            ticks="always"
            tick-size="5"
          ></v-range-slider>
        </v-col>
        <v-col cols="1">
          <v-btn
            style="text-transform: none"
            color="primary"
            dark
            @click="submit"
          >
            MatchOn!
          </v-btn>
        </v-col>
      </v-row>
      <p>{{ sportsName }}</p>
      <p>{{ date1 }}</p>
      <p>{{ time }}</p>
    </v-container>
  </v-form>
</template>

<script>
import http from "@/util/http-common";
import { mapState } from "vuex";

export default {
  name: "About",
  components: {},
  data() {
    return {
      sportsName: this.$route.params.sports,
      menu1: false,
      date1: "",
      time: [0, 1],
      ticksLabels: [
        6,
        7,
        8,
        9,
        10,
        11,
        12,
        13,
        14,
        15,
        16,
        17,
        18,
        19,
        20,
        21,
        22,
      ],
      today: "",
      lat: "37.5663",
      lng: "126.9779",
    };
  },
  computed: {
    ...mapState(["token"]),
  },
  methods: {
    submit() {
      const requestHeaders = {
        headers: {
          Authorization: "JWT " + this.token,
        },
      };
      this.time[0] += 6;
      this.time[1] += 6;
      if (this.time[0] < 10) {
        this.time[0] = "0" + this.time[0];
      }
      if (this.time[1] < 10) {
        this.time[1] = "0" + this.time[1];
      }
      console.log(this.time);
      http
        .post(
          "/match/bm/",
          {
            sports_name: this.sportsName,
            date: this.date1,
            start_time: this.time[0] + ":00",
            end_time: this.time[1] + ":00",
            lat: this.lat,
            lng: this.lng,
          },
          requestHeaders
        )
        .then((res) => {
          console.log(res);
        });
      this.$router.push("/matching");
    },
    getToday() {
      var today = new Date();
      var dd = today.getDate();
      var mm = today.getMonth() + 1;
      var yyyy = today.getFullYear();

      if (dd < 10) {
        dd = "0" + dd;
      }

      if (mm < 10) {
        mm = "0" + mm;
      }

      today = yyyy + "-" + mm + "-" + dd;
      this.today = today;
      this.date1 = today;
    },
  },
  mounted() {
    this.getToday();
  },
};
</script>

<style>
</style>