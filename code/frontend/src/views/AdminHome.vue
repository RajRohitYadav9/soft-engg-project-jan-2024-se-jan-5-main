<template>
    <div class="card-container">
      <Card
            title="New User Registered"
            @click="new_registered_users"
            :value="new_registered_users().toString()"
          ></Card>
          <Card
            title="Total Open Tickets"
            @click="total_open_tickets"
            :value="n_total_unresolved_tickets.toString()"
          ></Card>
          <Card
            title="Total Resolved Tickets"
            @click="total_resolved_tickets"
            :value="n_total_resolved_tickets.toString()"
          ></Card>
          <Card title="New Tickets Raised Today"
          @click = "new_tickets_today"
          :value="n_tickets_today.toString()"></Card>
          <Card
            title="New Tickets Raised This Week"
            @click="new_tickets_raised_this_week"
            :value="n_tickets_week.toString()"
          ></Card>
          <Card
            title="New Tickets Raised This Month"
            @click="new_tickets_raised_this_month"
            :value="n_tickets_month.toString()"
          ></Card>
    
          <Card title="Total Student" 
          @click = total_students
          :value="n_student.toString()"></Card>
          <Card title="Total Support Staff" 
          @click = total_support_staff
          :value="n_support.toString()"></Card>
          <Card title="Total Admin" 
          @click = total_admin
          :value="n_admin.toString()"></Card>

  </div>
  <DiscourseButton
      class="discourse-button"
      tooltipText="Go to Discourse">
  </DiscourseButton> 

</template>

<script>

import Card from "../components/Card";

import * as common from "../assets/common.js";
import * as utils from "../utils/index.js";
import DiscourseButton from "../buttons/DiscourseButton.vue";

export default {
name: "AdminHome",
components: {  Card, DiscourseButton },
data() {
  return {
    user_id: this.$store.getters.get_user_id,
    n_total_unresolved_tickets: 0,
    n_total_resolved_tickets: 0,
    n_tickets_today: 0,
    n_tickets_week: 0,
    n_tickets_month: 0,
    n_student: 0,
    n_support: 0,
    n_admin: 0,
    n_student_new: 0,
    n_support_new: 0,
    n_user_new: 0,
  };
},
created() {
  this.$store.dispatch("set_active_tab", "dashboard");
  fetch(common.ADMIN_API, {
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
        this.n_total_unresolved_tickets = data.message.n_total_unresolved_tickets;
        this.n_total_resolved_tickets = data.message.n_total_resolved_tickets;
        this.n_tickets_today = data.message.n_tickets_today;
        this.n_tickets_week = data.message.n_tickets_week;
        this.n_tickets_month = data.message.n_tickets_month;
        this.n_student = data.message.n_student;
        this.n_support = data.message.n_support;
        this.n_admin = data.message.n_admin;
        this.n_student_new = data.message.n_student_new;
        this.n_support_new = data.message.n_support_new;
      }
      if (data.category == "error") {
        utils.show_error_and_logout(this,data.message);
      }
    })
    .catch((error) => {
      utils.show_error_and_logout(this,error);

    });

    this.n_user_new = this.n_student_new + this.n_support_new;
  },
  mounted() {},
  methods: {
    new_registered_users: function () {
      this.n_user_new = this.n_student_new + this.n_support_new;
      return this.n_user_new;
    },
    // new_registered_users_u(){
    //   alert('New Users Registered')
    // },
    total_open_tickets(){
      alert('Total open Tickts')
    },
    total_resolved_tickets(){
      alert('Total Resolved Tickets')
    },
    new_tickets_raised_this_week(){
      alert('Total weekly Tickets')
    },
    new_tickets_raised_this_month(){
      alert('Total monthly Tickets')
    },
    new_tickets_today(){
      alert('Total daily Tickets')
    },
    total_students(){
      alert('total students')
    },
    total_support_staff(){
      alert('total support staff')
    },
    total_admin(){
      alert('total admin')
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

/* Style for the Discourse button */
.discourse-button {
position: fixed; /* Stay in the same place even when scrolling */
right: 20px; /* Distance from the right edge of the viewport */
bottom: 20px; /* Distance from the bottom edge of the viewport */
z-index: 1000; /* Ensure it's on top of other elements */
}
</style>
