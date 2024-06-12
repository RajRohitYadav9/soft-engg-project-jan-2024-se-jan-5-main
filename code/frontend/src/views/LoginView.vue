<template>
  <div>
    <button @click="openModal">Login</button>
    <LoginModal :display="showLoginModal" @close="closeModal" />
  </div>
</template>

<script>
import LoginModal from '../modals/LoginModal.vue';

export default {
  components: {
    LoginModal,
  },
  data() {
    return {
      showLoginModal: false,
    };
  },
  methods: {
    openModal() {
      this.showLoginModal = true;
    },
    closeModal() {
      this.showLoginModal = false;
    },
  },
};
</script>

<style scoped>
button {
  background-color: #4CAF50; /* Green */
  border: none;
  color: white;
  padding: 15px 32px;
  text-align: center;
  text-decoration: none;
  display: inline-block;
  font-size: 16px;
  margin: 4px 2px;
  cursor: pointer;
  border-radius: 5px;
}
</style>

<!-- <script>
import * as common from "../assets/common.js";

export default {
  name: "LoginView",
  components: {},
  data() {
    return {
      form: {
        email: "",
        password: "",
      },
      show: true,
    };
  },
  methods: {
    onSubmit: async function (event) {
      event.preventDefault();
      this.$log.info("Submitting Login form");
      this.form.password = btoa(this.form.password);

      fetch(common.AUTH_API_LOGIN, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(this.form),
      })
        .then((response) => response.json())
        .then((data) => {
          if (data.category == "success") {
            this.flashMessage.success({
              message: "Successfully logged in.",
            });

            // update store
            this.$store.dispatch("set_state_after_login", data.message);
            this.$store.dispatch("token_timeout_fn", {});
            this.$router.push(`/${data.message.role}-home`); //home page depends on role
          }
          if (data.category == "error") {
            this.flashMessage.error({
              message: data.message,
            });
          }
        })
        .catch((error) => {
          this.$log.error(`Error : ${error}`);
          this.flashMessage.error({
            message: "Internal Server Error",
          });
        });
    },
    onReset(event) {
      event.preventDefault();
      this.form.email = "";
      this.form.password = "";
      this.show = false;
      this.$nextTick(() => {
        this.show = true;
      });
    },
  },
};
</script>

<style></style> -->
