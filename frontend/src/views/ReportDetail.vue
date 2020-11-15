<template>
  <div>
    <v-card class="mx-auto" max-width="720">
      <v-container fluid>
        <h2>{{ sports_name }} 전적</h2>
        <v-row>
          <v-col
            v-for="card1 in report_detail_datas"
            :key="card1.date"
            cols="12"
          >
            <v-card style="padding: 16px">
              <p>날짜: {{ card1.date }}</p>
              <p>장소: {{ card1.gu }}</p>
              <p>시작시간: {{ card1.fixed_time | ChangeTime }}시</p>
              <p>결과: {{ card1.result }}</p>
            </v-card>
          </v-col>
        </v-row>
      </v-container>
    </v-card>
  </div>
</template>

<script>
import http from "@/util/http-common";

export default {
  name: "ReportDetail",
  components: {},
  data() {
    return {
      sports_name: "",
    };
  },
  props: {
    report_detail_datas: {
      type: Array,
    },
    sports_name: {
      type: String,
    },
  },
  filters: {
    ChangeTime(value) {
      return value.split(":")[0];
    },
  },
};
</script>

<style>
</style>