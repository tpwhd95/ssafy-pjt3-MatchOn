<template>
  <div class="home">
    <v-card class="mx-auto" max-width="1000">
      <v-container fluid>
        <v-row>
          <v-col v-for="card in cards" :key="card.title" :cols="card.flex">
            <v-card>
              <v-img
                :src="card.src"
                class="white--text align-end"
                gradient="to bottom, rgba(0,0,0,.1), rgba(0,0,0,.5)"
                height="200px"
                @click="matching"
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
      cards: [
        {
          title: "Futsal",
          src: "https://cdn.vuetifyjs.com/images/cards/house.jpg",
          flex: 6,
        },
        {
          title: "Favorite road trips",
          src: "https://cdn.vuetifyjs.com/images/cards/road.jpg",
          flex: 6,
        },
        {
          title: "Best airlines",
          src: "https://cdn.vuetifyjs.com/images/cards/plane.jpg",
          flex: 6,
        },
        {
          title: "Best airlines",
          src: "https://cdn.vuetifyjs.com/images/cards/plane.jpg",
          flex: 6,
        },
        {
          title: "Best airlines",
          src: "https://cdn.vuetifyjs.com/images/cards/plane.jpg",
          flex: 6,
        },
      ],
    };
  },
  methods: {
    matching() {
      this.$router.push("/About");
    },
  },
};
</script>
