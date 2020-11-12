<template>
  <v-card class="mx-auto" max-width="720">
    <h1>조율하는 방</h1>
    <p>{{ match_id }}번 경기</p>
    <p>방장: {{ room_master }}</p>
    <div class="card">
      <div class="card-body">
        <p class="text-secondary nomessages" v-if="messages.length == 0">
          [No messages yet!]
        </p>
        <div class="messages" v-chat-scroll="{ always: false, smooth: true }">
          <div v-for="message in messages" :key="message.id">
            <span class="text-info">[{{ message.name }}]: </span>
            <span>{{ message.message }}</span>
            <br />
            <span class="text-secondary time">{{ message.timestamp }}</span>
          </div>
        </div>
      </div>
      <div class="card-action">
        <CreateMessage :name="userProfile.username" :match_id="match_id" />
      </div>
    </div>
  </v-card>
</template>

<script>
import http from "@/util/http-common";
import { mapState } from "vuex";
import CreateMessage from "@/components/CreateMessage";
import fb from "@/firebase/init";
import moment from "moment";

export default {
  name: "MatchRoom",
  components: {
    CreateMessage,
  },
  data() {
    return {
      match_id: this.$route.query.match_id,
      room_master: null,
      center_lat: "",
      center_lng: "",
      messages: [],
      userProfile: sessionStorage.getItem("userProfile")
        ? JSON.parse(sessionStorage.getItem("userProfile"))
        : [],
    };
  },
  computed: {
    ...mapState(["token"]),
  },
  created() {
    this.getRoomData(this.match_id);

    let ref = fb
      .collection("messages" + String(this.match_id))
      .orderBy("timestamp");

    ref.onSnapshot((snapshot) => {
      snapshot.docChanges().forEach((change) => {
        if ((change.type = "added")) {
          let doc = change.doc;
          this.messages.push({
            id: doc.id,
            name: doc.data().name,
            message: doc.data().message,
            timestamp: moment(doc.data().timestamp).format("LTS"),
          });
        }
      });
    });
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

<style scoped>
.chat h2 {
  font-size: 2.6em;
  margin-bottom: 0px;
}

.chat h5 {
  margin-top: 0px;
  margin-bottom: 40px;
}

.chat span {
  font-size: 1.2em;
}

.chat .time {
  display: block;
  font-size: 0.7em;
}

.messages {
  max-height: 300px;
  overflow: auto;
}
</style>