<template>
      <LoadingAnimation v-show="loadingAnimation"></LoadingAnimation>
    <div v-show="!loadingAnimation">
  <FAQCard :faqs="faqs"></FAQCard>

  <FloatingFAQCreateButton v-if="admin" @faqCreated=refresh()></FloatingFAQCreateButton>
</div>
  </template>
  
  <script>
// Import your FAQmodal component
  import {FAQ_API} from "../assets/common.js";
  import * as utils from "../utils/index.js"
  import LoadingAnimation from '../layouts/LoadingAnimation.vue';

  import { defineAsyncComponent } from 'vue';


  export default {
    name: 'CommonFAQs',
    components: {
      LoadingAnimation,
      FAQCard : defineAsyncComponent(() => import('@/components/FAQCard.vue')),
      FloatingFAQCreateButton: defineAsyncComponent(() => import('@/components/FloatingFAQCreateButton.vue')),
    },
    data() {
      return {
        loadingAnimation: true,
        faqs: [],
        showDetails: false,
        selectedFaq: null,
      };
    },
    created() {
      // Fetch your FAQs here (replace with your data fetching logic)
      this.$store.dispatch("set_active_tab", "faqs");
      // this.faqs = [
      //   {
      //     id: 1,
      //     title: "What is Vue.js?",
      //     description: "Vue.js is a progressive JavaScript framework for building user interfaces. It is...",
      //     attachments: [],
      //   },
      //   // Add more FAQs here
      // ];

    },
    methods: {
      openFAQModal(faq) {
        this.showDetails = true;
        this.selectedFaq = faq;
      },

      async getFaqs() {
        await fetch(FAQ_API , {
          method: "GET",
          headers: {
          "Content-Type": "application/json",
          "Web-Token" : this.$store.getters.get_web_token,
          "User-Id" : this.$store.getters.get_user_id,
        },
        })
          .then((response) => response.json())
          .then((data) => {
            if (data.category == "success") {
              // this.flashMessage.success({
              //   message: `Total ${data.message.length} Tickets retrieved.`,
              // });
              this.faqs = data.message;
            }
            if (data.category == "error") {
              utils.show_error_and_logout(this,data.message);
            }
          })
          .catch(() => {
            this.$flashMessage.failureMessage("Internal Server Error");
            utils.show_error_and_logout(this,"error");
          });
          this.loadingAnimation = false;
      },
        async refresh(){
          this.loadingAnimation = true;
          await this.getFaqs();
          this.loadingAnimation = false;

        }
    },
    async mounted(){
      await this.getFaqs();
      this.loadingAnimation = false;
    },

    computed:{
      admin(){
        return this.$store.getters.get_user_role === "admin";
      }
    }

  };
  </script>
  
  <style scoped>
  .faq-container {
    display: flex;
    flex-wrap: wrap;
    gap: 1
  }
  </style>