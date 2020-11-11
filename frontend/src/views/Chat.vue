<template>
  <div class="chat">
    <form onsubmit="return sendMessage();">
      <input id="message" placeholder="Enter message" autocomplete="off" />
      <input type="submit" />
    </form>

    <ul id="messages"></ul>
  </div>
</template>

<script>
export default {
  data() {
    return {
      myName: "",
    };
  },
  methods: {
    entername() {
      this.myName = prompt("Enter yout name");
    },
    sendMessage() {
      var message = document.getElementById("message").value;

      firebase.database().ref("messages").push().set({
        sender: this.myName,
        message: message,
      });

      return false;

      //   firebase
      //     .database()
      //     .ref("messages")
      //     .on("child_added", function (snapshot) {
      //       var html = "";
      //       // give each message a unique ID
      //       html += "<li id='message-" + snapshot.key + "'>";
      //       // show delete button if message is sent by me
      //       if (snapshot.val().sender == myName) {
      //         html +=
      //           "<button data-id='" +
      //           snapshot.key +
      //           "' onclick='deleteMessage(this);'>";
      //         html += "Delete";
      //         html += "</button>";
      //       }
      //       html += snapshot.val().sender + ": " + snapshot.val().message;
      //       html += "</li>";

      //       document.getElementById("messages").innerHTML += html;
      //     });
    },
  },
  mounted() {
    this.entername();
  },
};
</script>

<style>
</style>