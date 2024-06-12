<template >
  <div class="home-div">
    <div class="style-0">
    <div class="style-1"></div>
    <h1 class="style-2">Welcome To Online Support Ticketing System</h1>
    <h2 class="style-3">Create, share, and 
        <!-- --><span class="style-4"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="24" height="24" class="style-5">
                <path d="M9.2467 3C9.65074 6.17905 12.5275 9.00324 15.6934 9.5C12.5275 9.99676 9.65074 12.8209 9.24669 16C8.84265 12.8209 6.16589 9.99676 3 9.5C6.16589 9.00324 8.84265 6.19877 9.2467 3.01971M17.3 20L17.2329 19.5924C17.0448 18.4504 16.1496 17.5552 15.0076 17.3671L14.6 17.3L15.0076 17.2329C16.1496 17.0448 17.0448 16.1496 17.2329 15.0076L17.3 14.6L17.3671 15.0076C17.5552 16.1496 18.4504 17.0448 19.5924 17.2329L20 17.3L19.5924 17.3671C18.4504 17.5552 17.5552 18.4504 17.3671 19.5924L17.3 20Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" fill="none" class="style-6"></path>
            </svg>solve</span> <!-- -->
    </h2>
    <div class="style-7"><input type="text" name="search" placeholder="Search for A Ticket" class="style-8" v-model="form.query" />
        <button @click="search()" class="style-9"><svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" class="style-10">
                <path d="M21 21L14.9497 14.9497M14.9497 14.9497C16.2165 13.683 17 11.933 17 10C17 6.13401 13.866 3 10 3C6.13401 3 3 6.13401 3 10C3 13.866 6.13401 17 10 17C11.933 17 13.683 16.2165 14.9497 14.9497Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="style-11"></path>
            </svg><span class="style-12">Search</span>
          </button>
        </div>

    </div>
        <TicketCard3 :tickets="tickets">
    </TicketCard3>

  </div>
</template>

<script>
import * as common from "../assets/common.js";
// import LoginModal from '../modals/LoginModal.vue';
// import RegisterModal from '../modals/RegisterModal';
import TicketCard3 from '../components/TicketCard3.vue';

function debounce(func, wait = 500) {
  let timeout;
  return (...args) => {
    clearTimeout(timeout);
    timeout = setTimeout(() => func.apply(this, args), wait);
  };
}

export default {
  name: "AppHomeView",
  // components: { LoginModal, RegisterModal},
  components: {
    TicketCard3
  },
  watch:{
        'form.query'(value){
            this.form.query = value;
            this.search();
        }
    },
  data() {
    return {
      show: true,
      showLoginModal: false,
      showRegisterModal: false,
      search_url: common.FEW_TICKETS,
      tickets: null,
      form: {
        query: "",
      }
    };
  },
  async mounted() {
    //this.fetchTickets();
    await this.load();
  },
  methods: {
    toggleLoginModal(){
      this.showRegisterModal = false;
      this.showLoginModal = !this.showLoginModal;
      
    },
    toggleRegisterModal(){
      this.showLoginModal = false;
      this.showRegisterModal = !this.showRegisterModal;
    },

    async load() {
      let params = new URLSearchParams(this.form).toString()
      console.log(params);
      await fetch(this.search_url + "?" + params,{
          method: "GET",
      })
        .then((response) => response.json())
        .then((data) => {
          if (data.category == "success") {
            this.tickets = data.message;
          }
        });
    },

    search(){
      const update = debounce(()=>{
            this.load();
        },500);
      update();
    }

  },
  computed: {
    noModal(){
      return !(this.showRegisterModal | this.showLoginModal)
    }
  }
};
</script>

<style scoped>

.style-0 {
        padding-top: 70px;
        margin-top: 0px;
        padding-bottom: 0px;
        padding-left: 16px;
        padding-right: 16px;
        justify-content: center;
        align-items: center;
        flex-direction: column;
        display: flex;
        margin-left: auto !important;
        margin-right: auto !important;
        position: relative;
        box-sizing: border-box;
        border-width: 0px;
        border-style: solid;
        border-color: rgb(229, 231, 235);
        margin: 0px;
    }

    .style-1 {
        bottom: -70px;
        filter: blur(100px);
        --tw-gradient-to: transparent 100% !important;
        --tw-gradient-from: transparent 0% !important;
        background-image: linear-gradient(rgba(0, 0, 0, 0) 0%, rgb(55, 65, 81) 95%, rgba(0, 0, 0, 0) 100%);
        border-radius: 9999px;
        /* transform: matrix(1, 0, 0, 1, -800, 0); */
        max-width: 1600px;
        width: 100% !important;
        height: 200px;
        /* left: 951.5px; */
        position: absolute;
        box-sizing: border-box;
        border-width: 0px;
        border-style: solid;
        border-color: rgb(229, 231, 235);
        padding: 0px;
        margin: 0px;
    }

    .style-2 {
        font-size: 60px;
        line-height: 60px;
        padding-left: 0px;
        padding-right: 0px;
        max-width: 784px;
        font-weight: 700;
        text-align: center;
        margin: 0px;
        box-sizing: border-box;
        border-width: 0px;
        border-style: solid;
        color:#f2f2f2;
        border-color: rgb(229, 231, 235);
        padding: 0px;
    }

    .style-3 {
        max-width: 390px;
        color: rgb(156, 163, 175);
        font-weight: 600;
        text-align: center;
        padding-left: 16px;
        padding-right: 16px;
        margin-top: 24px;
        /* z-index: 10; */
        margin: 24px 0px 0px;
        font-size: 16px;
        box-sizing: border-box;
        border-width: 0px;
        border-style: solid;
        border-color: rgb(229, 231, 235);
        padding: 0px 16px;
    }

    .style-4 {
        color: rgb(232, 121, 249);
        font-style: italic;
        gap: 4px;
        align-items: baseline;
        display: inline-flex;
        box-sizing: border-box;
        border-width: 0px;
        border-style: solid;
        border-color: rgb(229, 231, 235);
        padding: 0px;
        margin: 0px;
    }

    .style-5 {
        transform: matrix(1, 0, 0, 1, 0, 4);
        width: 1.25rem !important;
        height: 20px;
        display: block;
        vertical-align: middle;
        box-sizing: border-box;
        border-width: 0px;
        border-style: solid;
        border-color: rgb(229, 231, 235);
        padding: 0px;
        margin: 0px;
    }

    .style-6 {
        box-sizing: border-box;
        border-width: 0px;
        border-style: solid;
        border-color: rgb(229, 231, 235);
        padding: 0px;
        margin: 0px;
    }

    .style-7 {
        margin-bottom: -40px;
        transition-property: transform;
        transition-timing-function: cubic-bezier(0.4, 0, 0.2, 1);
        transition-duration: 0.15s;
        box-shadow: rgba(0, 0, 0, 0) 0px 0px 0px 0px, rgba(0, 0, 0, 0) 0px 0px 0px 0px, rgba(0, 0, 0, 0.1) 0px 10px 15px -3px, rgba(0, 0, 0, 0.1) 0px 4px 6px -4px;
        background-color: rgb(255, 255, 255);
        border-radius: 9999px;
        overflow: visible;
        max-width: 550px;
        width: 100% !important;
        display: flex;
        margin-top: 32px;
        /* z-index: 21; */
        position: relative;
        box-sizing: border-box;
        border-width: 0px;
        border-style: solid;
        border-color: rgb(229, 231, 235);
        padding: 0px;
    }

    .style-8 {
        box-shadow: rgba(0, 0, 0, 0) 0px 0px 0px 0px, rgba(0, 0, 0, 0) 0px 0px 0px 0px, rgba(0, 0, 0, 0.05) 0px 1px 2px 0px;
        color: rgb(8, 8, 8);
        font-weight: 400;
        font-size: 16px;
        line-height: 24px;
        font-family: Montserrat, ui-sans-serif, system-ui, sans-serif, 'Apple Color Emoji', 'Segoe UI Emoji', 'Segoe UI Symbol', 'Noto Color Emoji';
        padding-right: 8px;
        padding-left: 40px;
        padding-top: 16px;
        padding-bottom: 16px;
        background-color: rgb(255, 255, 255);
        border-style: none;
        border-start-start-radius: 9999px;
        border-end-start-radius: 9999px;
        width: 100% !important;
        display: block;
        margin-right: 1px;
        appearance: none;
        border-color: rgb(107, 114, 128);
        border-width: 0px;
        border-radius: 9999px 0px 0px 9999px;
        padding: 16px 8px 16px 40px;
        font-feature-settings: normal;
        font-variation-settings: normal;
        margin: 0px 1px 0px 0px;
        box-sizing: border-box;
    }

    .style-9 {
        transition-property: color, background-color, border-color, text-decoration-color, fill, stroke;
        transition-timing-function: cubic-bezier(0.4, 0, 0.2, 1);
        transition-duration: 0.15s;
        color: rgb(17, 17, 17);
        font-weight: 600;
        font-size: 16px;
        line-height: 24px;
        font-family: Montserrat, ui-sans-serif, system-ui, sans-serif, 'Apple Color Emoji', 'Segoe UI Emoji', 'Segoe UI Symbol', 'Noto Color Emoji';
        padding-right: 28px;
        padding-top: 6px;
        padding-bottom: 6px;
        padding-left: 20px;
        background-color: rgb(255, 255, 255);
        border-style: none;
        border-start-end-radius: 9999px;
        border-end-end-radius: 9999px;
        gap: 6px;
        align-items: center;
        cursor: pointer;
        display: flex;
        appearance: button;
        background-image: none;
        text-transform: none;
        font-feature-settings: normal;
        font-variation-settings: normal;
        margin: 0px;
        padding: 6px 28px 6px 20px;
        box-sizing: border-box;
        border-width: 0px;
        border-color: rgb(229, 231, 235);
    }

    .style-10 {
        transition-property: color, background-color, border-color, text-decoration-color, fill, stroke;
        transition-timing-function: cubic-bezier(0.4, 0, 0.2, 1);
        transition-duration: 0.15s;
        color: rgb(17, 17, 17);
        width: 1.25rem !important;
        height: 20px;
        display: block;
        vertical-align: middle;
        box-sizing: border-box;
        border-width: 0px;
        border-style: solid;
        border-color: rgb(229, 231, 235);
        padding: 0px;
        margin: 0px;
    }

    .style-11 {
        box-sizing: border-box;
        border-width: 0px;
        border-style: solid;
        border-color: rgb(229, 231, 235);
        padding: 0px;
        margin: 0px;
    }

    .style-12 {
        box-sizing: border-box;
        border-width: 0px;
        border-style: solid;
        border-color: rgb(229, 231, 235);
        padding: 0px;
        margin: 0px;
    }

    .style-13 {
        display: none;
        gap: 16px;
        justify-content: center;
        flex-wrap: wrap;
        margin-top: 32px;
        box-sizing: border-box;
        border-width: 0px;
        border-style: solid;
        border-color: rgb(229, 231, 235);
        padding: 0px;
        margin: 32px 0px 0px;
    }

    .style-14 {
        animation-duration: 0.2s;
        transition-duration: 0.2s;
        transition-property: color, background-color, border-color, text-decoration-color, fill, stroke;
        transition-timing-function: cubic-bezier(0.4, 0, 0.2, 1);
        color: rgb(242, 242, 242);
        font-weight: 600;
        font-size: 16px;
        line-height: 24px;
        font-family: Montserrat, ui-sans-serif, system-ui, sans-serif, 'Apple Color Emoji', 'Segoe UI Emoji', 'Segoe UI Symbol', 'Noto Color Emoji';
        padding-right: 48px;
        padding-left: 40px;
        padding-top: 12px;
        padding-bottom: 12px;
        background-color: rgb(79, 70, 229);
        border-style: none;
        border-radius: 8px;
        gap: 8px;
        align-items: center;
        cursor: pointer;
        max-width: fit-content;
        display: flex;
        margin-left: auto !important;
        margin-right: auto !important;
        /* z-index: 21; */
        position: relative;
        text-decoration: none solid rgb(242, 242, 242);
        box-sizing: border-box;
        border-width: 0px;
        border-color: rgb(229, 231, 235);
        padding: 12px 48px 12px 40px;
        margin: 0px auto;
    }

    .style-15 {
        width: 1.5rem !important;
        height: 24px;
        margin-right: 6px;
        display: block;
        vertical-align: middle;
        box-sizing: border-box;
        border-width: 0px;
        border-style: solid;
        border-color: rgb(229, 231, 235);
        padding: 0px;
        margin: 0px 6px 0px 0px;
    }

    .style-16 {
        box-sizing: border-box;
        border-width: 0px;
        border-style: solid;
        border-color: rgb(229, 231, 235);
        padding: 0px;
        margin: 0px;
    }

    .style-17 {
        animation-duration: 0.2s;
        transition-duration: 0.2s;
        transition-property: color, background-color, border-color, text-decoration-color, fill, stroke;
        transition-timing-function: cubic-bezier(0.4, 0, 0.2, 1);
        color: rgb(242, 242, 242);
        font-weight: 600;
        font-size: 16px;
        line-height: 24px;
        font-family: Montserrat, ui-sans-serif, system-ui, sans-serif, 'Apple Color Emoji', 'Segoe UI Emoji', 'Segoe UI Symbol', 'Noto Color Emoji';
        padding-right: 40px;
        padding-left: 32px;
        padding-top: 12px;
        padding-bottom: 12px;
        background-color: rgb(33, 33, 33);
        border-style: none;
        border-radius: 8px;
        gap: 16px;
        align-items: center;
        cursor: pointer;
        display: flex;
        text-decoration: none solid rgb(242, 242, 242);
        box-sizing: border-box;
        border-width: 0px;
        border-color: rgb(229, 231, 235);
        padding: 12px 40px 12px 32px;
        margin: 0px;
    }

    .style-18 {
        display: block;
        vertical-align: middle;
        box-sizing: border-box;
        border-width: 0px;
        border-style: solid;
        border-color: rgb(229, 231, 235);
        padding: 0px;
        margin: 0px;
    }

    .style-19 {
        box-sizing: border-box;
        border-width: 0px;
        border-style: solid;
        border-color: rgb(229, 231, 235);
        padding: 0px;
        margin: 0px;
    }
.home-div {
  /* background-image: url("../assets/home_page_image2.jpg"); */
  height: 100vh;
  /* background-position: center;
  background-repeat: no-repeat;
  background-size: cover; */
}
.logo{
  margin-top: 0;
  /* padding:20px; */
  /* text-align: center;  */
  /* font-size: var(--home-logo-text-size); */
  /* color: var(--home-logo-color); */
  /* background-color: var(--logo-bg-color); */
  /* backdrop-filter: blur(5px); */
  /* position: fixed; */
  width: 100%;
}

/* .login-button{
  float: right;
  margin-right:50px;
} */
/* }
.login-button button{
  background-color: var(--login-button-color);
  border: none;
  padding:10px 20px 10px 20px;
  font-size: var(--button-text-size);
  border-radius: var(--average-border-radius);
  color: var(--button-text-color);
} */
.login-button {
  width:14%;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  float: right;
  padding: 10px 20px;
  position: fixed;
  bottom: 4rem;
  left: 50%;
  transform: translateX(-50%);
  font-size: var(--normal-text-size);
  background-color: var(--login-button-color);
  color: var(--button-text-color);
  text-decoration: none;
  border-radius: var(--average-border-radius);
  transition: background-color 0.3s;
}

.login-button:hover {
  background-color: var(--login-button-hover-color);
}



</style>
