<template>
  <div class="home">
    <v-card class="mx-auto" max-width="720">
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
                @click="matching(card.title)"
                style="cursor: pointer"
              >
                <v-card-title v-text="card.title"></v-card-title>
              </v-img>

              <v-card-actions>
                <v-spacer></v-spacer>

                <v-btn icon>
                  <v-icon>mdi-heart</v-icon>
                </v-btn>

                <v-btn icon>
                  <v-icon>mdi-bookmark</v-icon>
                </v-btn>

                <v-btn icon>
                  <v-icon>mdi-share-variant</v-icon>
                </v-btn>
              </v-card-actions>
            </v-card>
          </v-col>
        </v-row>
      </v-container>
    </v-card>
  </div>
</template>

<script>
export default {
  name: "Home",
  components: {},
  data() {
    return {
      sportsName: "",
      cards: [
        {
          title: "풋살",
          src: "https://cdn.vuetifyjs.com/images/cards/house.jpg",
          flex: 12,
        },
        {
          title: "농구",
          src: "https://cdn.vuetifyjs.com/images/cards/road.jpg",
          flex: 12,
        },
        {
          title: "테니스",
          src: "https://cdn.vuetifyjs.com/images/cards/plane.jpg",
          flex: 12,
        },
        {
          title: "당구",
          src: "https://cdn.vuetifyjs.com/images/cards/plane.jpg",
          flex: 12,
        },
        {
          title: "볼링",
          src: "https://cdn.vuetifyjs.com/images/cards/plane.jpg",
          flex: 12,
        },
      ],
    };
  },
  methods: {
    matching(sportsName) {
      this.$router.push({ name: "About", params: { sports: sportsName } });
    },
  },
};
</script>
