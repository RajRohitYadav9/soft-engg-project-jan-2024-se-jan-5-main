
import router from '../router';
import createPersistedState from "vuex-persistedstate";


import { createStore } from 'vuex';

export const store = createStore({
  state () {
    return {
        user: {
            user_id: "",
            role: "",
            name: "",
            username: "",
            email: "",
            profile_photo_loc: "",
          },
        web_token: "",
        token_expiry_on: 0,
        token_validity:0,
        logged_status: false,
        timeout_id: null,
        active_tab: "",
    }
  },
  getters: {
    get_user(state) {
      return state.user
    },
    get_username(state) {
      return state.user.username
    },
    get_email(state){
      return state.user.email
    },
    get_user_id(state) {
      return state.user.user_id
    },
    get_user_role(state) {
      return state.user.role
    },
    get_user_profile_pic(state) {
      return state.user.profile_photo_loc
    },
    get_web_token(state) {
      return state.web_token
    },
    get_token_expiry_on(state) {
      return state.token_expiry_on
    },
    get_logged_status(state) {
      return state.logged_status
    },
    get_active_tab(state){
      return state.active_tab;
    },
  

  },
  plugins: [createPersistedState()],
  mutations: {
    initialiseStore(state) {
      // Check if the ID exists
      if (localStorage.getItem('store')) {
        console.log('App creating. Store available in local storage');
        // Replace the state object with the stored item
        this.replaceState(
          Object.assign(state, JSON.parse(localStorage.getItem('store')))
        );
      }
    },

    SET_STATE_AFTER_LOGIN(state, payload) {
      state.user.name = payload.name;
      state.user.username = payload.username;
      state.user.email = payload.email;
      state.user.user_id = payload.user_id;
      state.user.profile_photo_loc = payload["profile_photo_loc"];
      state.user.role = payload.role;
      state.web_token = payload.web_token;
      state.token_expiry_on = payload.token_expiry_on;
      state.token_validity = payload.token_validity;
      state.logged_status = true;
    },
    SET_STATE_AFTER_LOGOUT(state) {
      state.user.name = "";
      state.user.username = "";
      state.user.email = "";
      state.user.user_id = "";
      state.user.role = "";
      state.web_token = "";
      state.token_expiry_on = 0;
      state.token_validity = 0;
      state.user.profile_photo_loc = "";
      state.logged_status = false;
      clearTimeout(state.timeout_id);
    },
    SET_STATE_AFTER_PROFILE_PIC_UPDATE(state, payload) {
      state.user.profile_photo_loc = payload.profile_photo_loc;
    },
    SET_TIMEOUT_ID(state, payload) {
      state.timeout_id = payload;
    },
    SET_ACTIVE_TAB(state, payload) {
      state.active_tab = payload;
    },

  },
  actions: {
    set_state_after_login(context, payload) {
      context.commit('SET_STATE_AFTER_LOGIN', payload);
    },
    set_state_after_logout(context) {
      context.commit('SET_STATE_AFTER_LOGOUT');
    },
    set_state_after_profile_pic_update(context, payload) {
      context.commit('SET_STATE_AFTER_PROFILE_PIC_UPDATE', payload);
    },
    token_timeout_fn: async function (context) {
      // delete token after timeout
      const timeout_id = setTimeout(function () {
        alert("Token Expired. Please login again");
        context.commit('SET_STATE_AFTER_LOGOUT');
        router.push("/");
      }, context.state.token_validity * 1000);  // 1000 means 1 sec
      context.commit('SET_TIMEOUT_ID', timeout_id);
    },
    set_active_tab(context, payload){
      context.commit("SET_ACTIVE_TAB", payload);
    },
    save_filter(context, payload){
      context.commit("SAVE_FILTER", payload);
    }
  },
  },
)

export default store;