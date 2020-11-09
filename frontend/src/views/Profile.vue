<template>
  <div>
    <v-card class="mx-auto" max-width="720">
      <v-container fluid>
        <h2>{{ userProfile.username }}님의 경기 정보</h2>
        <v-row>
          <v-col v-for="card1 in cards1" :key="card1.title" :cols="card1.flex">
            <v-card>
              <h3>{{ card1.title }}</h3>
              <v-row>
                <v-col
                  v-for="card2 in card1.cards2"
                  :key="card2.sports"
                  :cols="card2.flex"
                >
                  <v-card>
                    <p>{{ card2.sports }}</p>
                    <p>{{ card2.date }}</p>
                  </v-card>
                </v-col>
              </v-row>
            </v-card>
          </v-col>
        </v-row>
      </v-container>
    </v-card>
  </div>
</template>

<script>
export default {
  name: "Profile",
  components: {},
  data() {
    return {
      userProfile: sessionStorage.getItem("userProfile")
        ? JSON.parse(sessionStorage.getItem("userProfile"))
        : [],
      cards1: [
        {
          title: "매칭중인 경기",
          flex: 12,
          cards2: [
            {
              sports: "풋살",
              date: "2020-11-18",
              flex: 12,
            },
            {
              sports: "풋살",
              date: "2020-11-21",
              flex: 12,
            },
          ],
        },
        {
          title: "조율중인 경기",
          flex: 12,
          cards2: [
            {
              sports: "풋살",
              date: "2020-11-15",
              flex: 12,
              src: "",
            },
          ],
        },
        {
          title: "대기중인 경기",
          flex: 12,
          cards2: [
            {
              sports: "풋살",
              date: "2020-11-11",
              flex: 12,
            },
          ],
        },
        {
          title: "완료된 경기",
          flex: 12,
          cards2: [
            {
              sports: "풋살",
              date: "2020-11-01",
              flex: 12,
              src: "",
            },
          ],
        },
      ],
    };
  },
};
</script>

<style>
</style>