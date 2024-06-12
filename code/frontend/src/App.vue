<template>
  <div id="app">
    <FlashMessage ref="flashMessage" />
    <!-- <NavBar></NavBar> -->
    <MainLayout2></MainLayout2>
  </div>
</template>

<script>
// import NavBar from "./components/NavBar"
import MainLayout2 from "./layouts/MainLayout2";
import FlashMessage from './custom_modules/FlashMessage.vue';

const debounce = (callback, delay) => {
    let tid;
    
    return function (...args) {
        const ctx = self;
        tid && clearTimeout(tid);
        tid = setTimeout(() => {
            callback.apply(ctx, args);
        }, delay);
      };
};

const _ = window.ResizeObserver;
  window. ResizeObserver = class ResizeObserver extends _ {
  constructor(callback) {
  callback = debounce (callback, 20);
  super(callback);
  }
};


export default {
  components: {FlashMessage, MainLayout2},
  data() {
    return {};
  },
  beforeCreate() {
    console.debug("Creating app.");
    this.$store.commit("initialiseStore");
  },
  mounted() {
    
  },
  methods: {},
  computed: {},
};
</script>

<style>
@import url("https://fonts.googleapis.com/css2?family=Roboto+Mono:wght@400;500&display=swap");
@import url("https://fonts.googleapis.com/icon?family=Material+Icons");
@import url("https://fonts.googleapis.com/icon?family=Material+Symbols+Outlined");
html{
  background-color: var(--maindark);
}
body {
  margin: 0;
  line-height: normal;
}
#app {
  /* font-family: Avenir, Helvetica, Arial, sans-serif; */
  font-family: "Roboto Mono", monospace;
  font-optical-sizing: auto;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: start;
  color: #2c3e50;
}

:root{
  --home-logo-color: white;
  --logo-bg-color:rgba(0, 85, 255, 0.331);
  --home-logo-text-size: 2rem;
  --normal-text-size: 1.4rem;
  --medium-text-size:1rem;
  --login-button-color: #007bff;
  --login-button-hover-color: #0056b3;
  --button-text-color: white;
  --average-border-radius: 30px;
  --button-text-size: large;
  --login-modal-button-color:#4caf50;
  --login-modal-button-color-hover:#3e8e41;
  --small-text-size: 1em;
  --smallest-text-size: 0.8rem;
  --dynamic-large-font-size: min(var(--normal-text-size),calc(40% + 2vw));
  --dynamic-small-font-size: min(var(--small-text-size),calc(15% + 2vw));
  --card-background-color: #313131;
  --card-text-color: rgb(79 255 138);
  --maindark: #171717;
  --dark:  #0e0e0e;
  --modal-color: rgb(49 46 46);
  --modal-border-color: #f2f2f2;
  --dark-button-color: #101010;
  --dark-button-hover-color: #000000;
  --h1-text-size: 24px;
}

/* Hide the default scrollbar */
::-webkit-scrollbar {
  width: 1px;
  height: 1px;
}

/* Track style */
::-webkit-scrollbar-track {
  background: #f1f1f1; /* Light grey background */
  border-radius: 10px; /* Rounded corners */
}

/* Thumb style */
::-webkit-scrollbar-thumb {
  background: #888; /* Dark grey thumb */
  border-radius: 10px; /* Rounded corners */
}

/* Add hover effect to thumb */
::-webkit-scrollbar-thumb:hover {
  background: #666; /* Darker grey on hover */
}

/* input:-webkit-autofill,
input:-internal-autofill-selected {
  color:#f2f2f2;
  -webkit-transition: background-color 5000s ease-in-out 0s;
  transition: background-color 5000s ease-in-out 0s;
}

input:hover:-webkit-autofill,
input:focus:-webkit-autofill,
input:hover:-internal-autofill-selected,
input:focus:-internal-autofill-selected {
  color:#f2f2f2;
  -webkit-transition-delay: 0s;
  transition-delay: 0s;
} */

.vuepress-markdown-body {
    background-color: var(--maindark) !important;
    color: #f2f2f2 !important;
}
.scrollbar__wrap {
    background-color: var(--maindark) !important;
}
.v-md-textarea-editor{
  height:98vh !important;
}

@media only screen and (min-width: 768px) { /* For screens wider than 768px */
    .v-md-editor.v-md-editor--editable {
        height: 20vh;
    }
}

@media only screen and (max-width: 767px){
  .v-md-editor.v-md-editor--editable {
          height: 40vw;
  }
  .style-8{
    font-size: 12px !important;
  }
  .style-2{
    font-size: 32px !important;
    line-height: 40px !important;
  }
  .card-content{
    padding-top: 10vh !important;
  }
  .search-component{
    right: 4rem !important;
  }
}

.material-icons {
    font-size: 16px !important;
}
.material-symbols-outlined {
    color: #f2f2f2 !important;
}

</style>
