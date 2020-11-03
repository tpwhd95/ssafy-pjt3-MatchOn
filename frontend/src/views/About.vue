<template>
  <v-form v-model="valid">
    <v-container>
      <v-row>
        <v-col cols="12" md="3">
          <v-text-field v-model="sports" label="Sports" required></v-text-field>
        </v-col>
        <v-col cols="12" md="3">
          <v-text-field v-model="date" label="Date" required></v-text-field>
        </v-col>
        <v-col cols="12" md="3">
          <v-text-field
            v-model="location"
            label="Location"
            required
          ></v-text-field>
        </v-col>
        <v-col cols="12" md="3">
          <v-btn class="mr-4" @click="submit"> submit </v-btn>
        </v-col>
      </v-row>
    </v-container>
  </v-form>
</template>

<script>
import http from "@/util/http-common";

export default {
  name: "About",
  components: {},
  data() {
    return {
      sports: "",
      start_time: "",
      end_time: "",
      lat: "",
      lng: "",
    };
  },
  methods: {
    submit() {
      http
        .post("/bm", {
          sports: this.sports,
          start_time: this.start_time,
          end_time: this.end_time,
          lat: this.lat,
          lng: this.lng,
        })
        .then((res) => {
          this.logs = res;
        });
    },
  },
};
</script>

<style>
</style>