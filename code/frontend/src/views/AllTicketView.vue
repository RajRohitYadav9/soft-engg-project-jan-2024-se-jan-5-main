<template>
    <LoadingAnimation v-show="loadingAnimation"></LoadingAnimation>
    <div v-show="!loadingAnimation">
      <div class="hide-this-on-scroll">
        <SearchComponent @searched="searchQuery"></SearchComponent>
        <FilterIcon @click="toggleFilterModal"></FilterIcon>
      </div>
    <TicketCard3 :tickets="ticket_card_details">
    </TicketCard3>
    <keep-alive>
      <FilterModal :filters="filters" v-if="showFilterModal" @close="toggleFilterModal" @filtered="filtered"></FilterModal>
    </keep-alive>
    </div>
    
    <DiscourseButton
        class="discourse-button"
        tooltipText="Go to Discourse">
    </DiscourseButton>
</template>

<script>
import FilterIcon from "@/assets/FilterIcon.vue"
import LoadingAnimation from '../layouts/LoadingAnimation.vue';
import SearchComponent from '../components/SearchComponent.vue';
import DiscourseButton from "../buttons/DiscourseButton.vue";


import * as common from "../assets/common.js";
import * as utils from "../utils/index.js"

import { defineAsyncComponent } from "vue";

export default {
  name: "AllTicketView",
  components: {
    LoadingAnimation,
    DiscourseButton,
    SearchComponent,
    TicketCard3 : defineAsyncComponent(() => import("@/components/TicketCard3.vue")),
    FilterModal : defineAsyncComponent(() => import("@/modals/FilterModal.vue")),
    FilterIcon },
  data() {
    return {
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
      loadingAnimation: true,
      ticket_card_details: [],
      user_role: this.$store.getters.get_user_role,
      current_page_path: this.$route.path,
      search_url: common.TICKET_API_ALLTICKETS,
      showFilterModal: false,
    };
    
  },
  methods: {
    async load() {
      // convert form to query params

      let params = new URLSearchParams(this.filters).toString();

      await fetch(this.search_url + "?" + params, {
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
            this.$flashMessage.failureMessage(data.message);
            this.$store.dispatch("set_state_after_logout");
            this.$router.push("/");
          }
        })
        .catch(() => {
          utils.show_error_and_logout(this,"Internal Server Error");
        });
        return 0;
    },
    toggleFilterModal(){
      this.showFilterModal = !this.showFilterModal;
    },
    async filtered(value){
      this.filters = value;
      this.showFilterModal = false,
      this.loadingAnimation = true;
      await this.load();
      this.loadingAnimation = false;
    },
    async searchQuery(value){
      this.filters.query = value;
      this.load();
    },
  },
  created(){
    this.$store.dispatch("set_active_tab", "all_tickets");
  },

  async mounted(){
    await this.load();
    this.loadingAnimation = false;
  },
  computed: {},
};
</script>

<style></style>
