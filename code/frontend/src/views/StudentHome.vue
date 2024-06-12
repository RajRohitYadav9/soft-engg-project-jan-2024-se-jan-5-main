<template>
    <LoadingAnimation v-show="loadingAnimation"></LoadingAnimation>
    <div v-show="!loadingAnimation">
    <SearchComponent @searched="searchQuery"></SearchComponent>
    <FilterIcon @click="toggleFilterModal"></FilterIcon>
    <TicketCard3 v-show="ticket_available" :tickets="ticket_card_details"></TicketCard3>
    <div v-show="no_ticket" class="no_ticket">
      No Tickets Availabe . Raise a new one
    </div>

    <div class="buttons-container">
      <DiscourseButton
        class="discourse-button"
        tooltipText="Go to Discourse">
    </DiscourseButton> 
    </div>

    <FloatingCreateButton @ticketCreated=refresh()></FloatingCreateButton>
    <keep-alive>
      <FilterModal :filters="filters" v-if="showFilterModal" @close="toggleFilterModal" @filtered="filtered"></FilterModal>
    </keep-alive>
  </div>
</template>

<script>
// 
import LoadingAnimation from '../layouts/LoadingAnimation.vue';
import SearchComponent from '../components/SearchComponent.vue';
import {TICKET_API_ALLTICKETS} from "../assets/common.js";
import {show_error_and_logout} from "../utils/index.js"

import { defineAsyncComponent } from 'vue';

export default {
  name: "StudentHome",
  components: {
    LoadingAnimation,
    SearchComponent,
    FilterIcon: defineAsyncComponent(() => import('@/assets/FilterIcon.vue')),
    TicketCard3: defineAsyncComponent(() => import('@/components/TicketCard3.vue')),
    FloatingCreateButton: defineAsyncComponent(() => import('@/components/FloatingCreateButton.vue')),
    FilterModal: defineAsyncComponent(() => import('@/modals/FilterModal.vue')),
    DiscourseButton: defineAsyncComponent(() => import('@/buttons/DiscourseButton.vue')),

  },
  data() {
    return {
      loadingAnimation: true,
      showFilterModal: false,
      n_tickets_created: 0,
      n_tickets_resolved: 0,
      n_tickets_pending: 0,
      n_tickets_upvoted: 0,
      user_id: this.$store.getters.get_user_id,
      filters: {
          query: "",
          filter_tags: [],
          filter_status: "",
          filter_priority: "",
          sortby: "",
          sortdir:"",
      },
      // ticket_card_details: [],
      ticket_card_details: null,
      user_role: this.$store.getters.get_user_role,
      current_page_path: this.$route.path,
      // user_id: this.$store.getters.get_user_id,
      search_url: TICKET_API_ALLTICKETS,
    };
    
  },
  methods: {
    async getTickets() {
      // convert form to query params
  
      let params = new URLSearchParams(this.filters).toString();

      await fetch(this.search_url + "/user" + "?" + params, {
        method: "GET",
        headers: {
        "Content-Type": "application/json",
        "Web-Token" : this.$store.getters.get_web_token,
        "User-Id" : this.user_id,
      },
      })
        .then((response) => response.json())
        .then((data) => {
          if (data.category == "success") {

            this.ticket_card_details = data.message;
          }
          if (data.category == "error") {
            show_error_and_logout(this,data.message);
          }
        })
        .catch(() => {
          show_error_and_logout(this,"Internal Server Error");

        });
      return 0;

    },

    async searchQuery(value){
      this.filters.query = value;
      this.getTickets();
    },


    async refresh(){
      this.loadingAnimation = true;
      this.getTickets();
      this.loadingAnimation = false;

    },
    toggleFilterModal(){
      this.showFilterModal = !this.showFilterModal;
    },
    async filtered(value){
      this.filters = value
      this.showFilterModal = false;
      this.refresh()
    }

  },
  created(){
      this.$store.dispatch("set_active_tab", "my_tickets");
  },

  async mounted(){
    
    await this.getTickets();
    this.loadingAnimation = false;

  },
  computed: {
    no_ticket(){
      return this.ticket_card_details != null && this.ticket_card_details.length == 0;
    },
    ticket_available(){
      return this.ticket_card_details != null && this.ticket_card_details.length > 0;
    }
  },
};
</script>

<style scoped>
.buttons-container {
    display: flex; /* Ensures elements are lined up horizontally */
    gap: 16px; /* Provides space between the buttons */
    position: fixed; /* Keeps the button container fixed at a location */
    right: 20px; /* Adjusted for visibility and to avoid overlap with other elements */
    bottom: 20px; /* Same as above */
    z-index: 1000; /* Ensures the container is above most other elements */
}

.buttons-container > * {
    transition: transform 0.3s ease; /* Smooth transition for hover effects */
}

.buttons-container > *:hover {
    transform: translateY(-5px); /* Subtle lift effect to indicate interactivity */
    cursor: pointer; /* Changes the cursor to a pointer to indicate clickable items */
}

.no_ticket {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    color: rgb(156, 0, 217);
}
</style>