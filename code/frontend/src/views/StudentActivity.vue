<template>
    <div class="card-container">
          <Card
            title="Total Tickets"
            @click="show_all_ticket"
            :value="n_tickets_created.toString()"
          ></Card>
          <Card
            title="Total Resolved Tickets"
            @click="show_resolved_tickets"
            :value="n_tickets_resolved.toString()"
          ></Card>
          <Card 
            title="Tickets Pending" 
            @click="show_pending_tickts"
            :value="n_tickets_pending.toString()">
        </Card>
          <Card
            title="Total Tickets Upvoted"
            @click="show_total_tickets_upvoted"
            :value="n_tickets_upvoted.toString()"
          ></Card>
    </div>
</template>
  
  <script>
  
  import Card from "../components/Card";
  import {STUDENT_API} from "../assets/common.js";
  import * as utils from "../utils/index.js";
// import { RouterView } from "vue-router";
  
  
  export default {
  name: "StudentActivity",
  components: {  Card },
  data() {
    return {
      user_id: this.$store.getters.get_user_id,
      n_tickets_created : "",
      n_tickets_resolved: "",
      n_tickets_pending: "",
      n_tickets_upvoted: "",
    };
  },
  created() {
    this.$store.dispatch("set_active_tab", "activity");
    fetch(STUDENT_API, {
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
            this.n_tickets_created = data.message.n_tickets_created;
            this.n_tickets_resolved = data.message.n_tickets_resolved;
            this.n_tickets_pending = data.message.n_tickets_pending;
            this.n_tickets_upvoted = data.message.n_tickets_upvoted;
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
    show_all_ticket(){
      //alert(this.user_id)
      this.$router.push('/all-tickets');
    },
    show_resolved_tickets(){
      alert('Showing Resolved Tickets!')
    },
    show_pending_tickts(){
      alert("Showing Pending Tickets!")
    },
    show_total_tickets_upvoted(){
      alert("Showing Total upvoted Tickets!")
    }

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
