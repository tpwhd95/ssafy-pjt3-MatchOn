<template>
  <v-container>
    <v-btn
      v-if="!this.isLoggedIn"
      class="ml-2"
      min-width="0"
      text
      @click="login"
    >
      login
    </v-btn>

    <!-- profile -->
    <v-btn
      v-if="this.isLoggedIn"
      class="ml-2"
      min-width="0"
      text
      @click="login"
    >
      profile
    </v-btn>

    <!-- logout -->
    <v-btn
      v-if="this.isLoggedIn"
      class="ml-2"
      min-width="0"
      text
      @click="logout2"
    >
      logout
    </v-btn>
  </v-container>
</template>

<script>
import LoginForm from "@/views/LoginForm.vue";
import { mapGetters, mapActions } from "vuex";

export default {
  name: "LoginForm",
  components: {
    LoginForm,
  },
  props: {
    value: {
      type: Boolean,
      default: false,
    },
  },
  data() {
    return {
      dialog: false,
      login_profile: "login",
    };
  },
  created() {},
  computed: {
    ...mapGetters(["isLoggedIn"]),
  },

  methods: {
    login() {
      if (this.isLoggedIn) {
        this.$router.push("/");
        this.login_profile = "profile";
      } else {
        this.dialog = true;
      }
    },
    ...mapActions(["logout"]),
    logout2() {
      if (this.isLoggedIn) {
        this.logout();
        this.login_profile = "login";
        this.$router.push("/");
      }
    },
  },
};
</script>

<style>
</style>