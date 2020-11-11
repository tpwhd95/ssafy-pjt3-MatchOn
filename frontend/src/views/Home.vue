<template>
  <div class="home">
    <v-card v-if="!this.isLoggedIn" class="mx-auto" max-width="720">
      <v-container fluid> 로그인 하세요. </v-container>
    </v-card>

    <v-card v-if="this.isLoggedIn" class="mx-auto" max-width="720">
      <v-container fluid>
        <v-row>
          <v-col
            v-for="card in cards"
            :key="card.title"
            :cols="card.flex"
            :sportsName="card.title"
          >
            <v-card>
              <v-img
                :src="card.src"
                class="white--text align-end"
                gradient="to bottom, rgba(0,0,0,.1), rgba(0,0,0,.5)"
                height="200px"
                @click="matching(card.title, card.title2)"
                style="cursor: pointer"
              >
                <v-card-title v-text="card.title2"></v-card-title>
              </v-img>
            </v-card>
          </v-col>
        </v-row>
      </v-container>
    </v-card>
  </div>
</template>

<script>
import { mapGetters } from "vuex";

export default {
  name: "Home",
  components: {},
  data() {
    return {
      sportsName: "",
      cards: [
        {
          title: "futsal",
          title2: "풋살",
          src: require("@/assets/futsal.jpg"),
          flex: 12,
        },
        {
          title: "basket_ball",
          title2: "농구",
          src: require("@/assets/basketball.jpg"),
          flex: 12,
        },
        {
          title: "tennis",
          title2: "테니스",
          src: require("@/assets/tennis.jpg"),
          flex: 12,
        },
        {
          title: "pool",
          title2: "당구",
          src: require("@/assets/pool.jpg"),
          flex: 12,
        },
        {
          title: "bowling",
          title2: "볼링",
          src: require("@/assets/bowling.jpg"),
          flex: 12,
        },
      ],
    };
  },
  methods: {
    matching(sportsName, sportsNameKR) {
      this.$router.push({
        name: "About",
        params: { sports: sportsName, sportsKR: sportsNameKR },
      });
    },
  },
  computed: {
    ...mapGetters(["isLoggedIn"]),
  },
};
</script>
