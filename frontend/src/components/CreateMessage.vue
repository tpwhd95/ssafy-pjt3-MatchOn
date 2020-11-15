<template>
  <div class="container" style="margin-bottom: 30px">
    <form @submit.prevent="createMessage">
      <div class="form-group">
        <input
          type="text"
          name="message"
          class="form-control"
          placeholder="Enter message ..."
          v-model="newMessage"
        />
        <p class="text-danger" v-if="errorText">{{ errorText }}</p>
      </div>
      <v-btn class="btn btn-primary" type="submit" name="action"
        >메시지 전송</v-btn
      >
    </form>
  </div>
</template>

<script>
import fb from "@/firebase/init";

export default {
  name: "CreateMessage",
  props: ["name", "match_id"],
  data() {
    return {
      newMessage: null,
      errorText: null,
    };
  },
  methods: {
    createMessage() {
      if (this.newMessage) {
        fb.collection("messages" + String(this.match_id))
          .add({
            message: this.newMessage,
            name: this.name,
            timestamp: Date.now(),
          })
          .catch((err) => {
            console.log(err);
          });
        this.newMessage = null;
        this.errorText = null;
      } else {
        this.errorText = "A message must be entered first!";
      }
    },
  },
};
</script>

