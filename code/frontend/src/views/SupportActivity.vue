<template>
    <div class="card-container">

          <Card
            title="Total Resolved Tickets"
            :value="n_tickets_resolved.toString()"
          ></Card>
          <Card 
            title="Total Unresolved Tickets" 
            :value="n_total_unresolved_tickets.toString()">
        </Card>
    </div>
</template>
  
  <script>
  
  import Card from "../components/Card";
  import {SUPPORT_API} from "../assets/common.js";
  import * as utils from "../utils/index.js";
  
  
  export default {
  name: "SupportActivity",
  components: {  Card },
  data() {
    return {
      user_id: this.$store.getters.get_user_id,
      n_tickets_resolved : "",
      n_total_unresolved_tickets: "",
    };
  },
  created() {
    this.$store.dispatch("set_active_tab", "activity");
    fetch(SUPPORT_API, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        "Web-Token": this.$store.getters.get_web_token,
        "User-Id": this.$store.getters.get_user_id,
      },
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.status == 200) {
          this.$flashMessage.successMessage(
           "User data retrieved."
          );
        
            this.n_tickets_resolved = data.message.n_tickets_resolved;
            this.n_total_unresolved_tickets = data.message.n_total_unresolved_tickets;
        }
        if (data.category == "error") {
          utils.show_error_and_logout(this,data.message);
        }
      })
      .catch((error) => {
        this.$flashMessage.failureMessage(
          // "Internal Server Error"
          error
        );

      });

    this.n_user_new = this.n_student_new + this.n_support_new;
  },
  mounted() {},
  methods: {
  },
  computed: {},
};
</script>

<style>
.card-container{
  display: flex;
  align-items: flex-start;
  flex-wrap:wrap;
  gap: 100px;
  justify-content: space-around;
  padding-left:40px;
  padding-right:40px;
  padding:5vw;
}
</style>
