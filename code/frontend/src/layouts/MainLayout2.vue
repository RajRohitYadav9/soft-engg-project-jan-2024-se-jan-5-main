<template>
    <header>
        <img src="@/assets/logo1.png" alt="logo" class="logo">
        <nav>
            <ul class="navlinks" >
                <li class="items" :class="{active: isActive('my_tickets')}" @click="go(`/${role}-home`)"  v-if="role == 'student'" >My Tickets</li>
                <li class="items" :class="{active: isActive('dashboard')}" @click="go(`/${role}-home`)" v-if="role == 'admin'" >Dashboard</li>
                <li class="items" :class="{active: isActive('validate_users')}" @click="go('/admin-validate-users')" v-if="role == 'admin'" >Validate Users</li>
                <li class="items" :class="{active: isActive('all_tickets')}" @click="go('/all-tickets')" v-if="role == 'student' | role == 'admin'"  >All Tickets</li>
                <li class="items" :class="{active: isActive('all_tickets')}" @click="go(`/${role}-home`)" v-if="role == 'support'"  >All Tickets</li>
                <li class="items" :class="{active: isActive('faqs')}" @click="go('/faqs')" v-if="logged_status" >FAQ</li>
                <li class="items" :class="{active: isActive('activity')}" @click="go(`/${role}-activity`)" v-if="logged_status && role != 'admin'" >Activity</li>
                <li class="items" :class="{active: isActive('manage')}" @click="go('/admin/manage')" v-if="role == 'admin'" >Manage</li>
                <li class="items" v-if="!logged_status" @click="toggleLoginModal()">Login</li>
                <li class="items" v-if="logged_status" @click="toggleLogoutModal()">Logout</li>
                <li class="items" v-if="!logged_status" @click="toggleRegisterModal()">Sign Up</li>
                <li @click="showSidebar()"><ion-icon name="menu-outline"></ion-icon></li>
                <li class="items profile" :class="{active: isActive('profile')}" v-if="logged_status" ><img class="profile-pic" @click="go('/profile')" :src="profile_pic" alt="Profile Picture"></li>
            </ul>


            <ul class="sidebar">
                <li @click="closeSidebar()"><ion-icon name="close-outline"></ion-icon></li>
                <li :class="{active: isActive('my_tickets')}" @click="go(`/${role}-home`)"  v-if="role == 'student'" >My Tickets</li>
                <li :class="{active: isActive('dashboard')}" @click="go(`/${role}-home`)" v-if="role == 'admin'" >Dashboard</li>
                <li :class="{active: isActive('validate_users')}" @click="go('/admin-validate-users')" v-if="role == 'admin'" >Validate Users</li>
                <li :class="{active: isActive('all_tickets')}" @click="go('/all-tickets')" v-if="role == 'student' | role == 'admin'"  >All Tickets</li>
                <li :class="{active: isActive('all_tickets')}" @click="go(`/${role}-home`)" v-if="role == 'support'"  >All Tickets</li>
                <li v-if="logged_status" :class="{active: isActive('faqs')}" @click="go('/faqs')">FAQ</li>
                <li v-if="logged_status && role != 'admin'" :class="{active: isActive(`activity`)}" @click="go(`/${role}-activity`)" >Activity</li>
                <li :class="{active: isActive('manage')}" @click="go('/admin/manage')" v-if="role == 'admin'" >Manage</li>
                <li  v-if="!logged_status" @click="toggleLoginModal()">Login</li>
                <li v-if="logged_status" @click="toggleLogoutModal()">Logout</li>
                <li  v-if="!logged_status" @click="toggleRegisterModal()">Sign Up</li>
                <li v-if="logged_status" :class="{active: isActive('profile')}" ><img class="profile-pic" @click="go('/profile')" :src="profile_pic" alt="Profile Picture"></li>
            </ul>
        </nav>
        
    </header>
    <LoginModal :display="showLoginModal" @close="toggleLoginModal()" @go_register="toggleRegisterModal()" @forgot_password="toggleForgotPasswordModal()" />
    <RegisterModal :display="showRegisterModal" @close="toggleRegisterModal()" @reg_success="toggleLoginModal()" ></RegisterModal>
    <LogoutModal v-if="showLogoutModal" @logout="userLogout" @close="toggleLogoutModal"></LogoutModal>
    <ForgotPasswordModal v-if="showForgotPasswordModal" @close="toggleForgotPasswordModal()" ></ForgotPasswordModal>
    <main class="main">
      <router-view />
    </main>
</template>

<script>
// import { menu } from "@ionic/vue"
// import { IonMenuButton } from "@ionic/vue"
import {logout} from "../utils/index.js"

import {defineAsyncComponent} from 'vue';

export default {
  components: { 
    LoginModal: defineAsyncComponent(() => import("../modals/LoginModal.vue")),
    LogoutModal: defineAsyncComponent(() => import("../modals/LogoutModal.vue")),
    RegisterModal : defineAsyncComponent(() => import("../modals/RegisterModal.vue")),
    ForgotPasswordModal: defineAsyncComponent(() => import("../modals/ForgotPasswordModal.vue")),
},
    data(){
        return {
          hide_navbar: false,
          showLoginModal: false,
          showLogoutModal: false,
          showRegisterModal: false,
          sideBar: false,
          showForgotPasswordModal: false,

        }
    },
    methods: {
      isActive(nav_bar){
        return this.$store.getters.get_active_tab == nav_bar;
      },
      go(path){
        this.closeSidebar()
        this.$router.push(path);
      },
      showSidebar() {
        this.sideBar = true;
        const sidebar = document.querySelector(".sidebar");
        sidebar.style.display = 'flex';
        setTimeout(() => {
            sidebar.style.transform = 'translateX(0)'; 
        }, 10);
    },
    userLogout(){
        this.toggleLogoutModal()
        logout(this)
    },

    closeSidebar() {
        this.sideBar = false;
        const sidebar = document.querySelector(".sidebar");
        sidebar.style.transform = 'translateX(100%)'; 
        setTimeout(() => {
            sidebar.style.display = 'none';
            }, 300);
    },

    toggleLoginModal(){
            this.showRegisterModal = false;
            this.showLoginModal = !this.showLoginModal;
            this.closeSidebar()
        
    },
    toggleLogoutModal(){
            this.showRegisterModal = false;
            this.showLoginModal = false;
            this.showLogoutModal = !this.showLogoutModal,
            this.closeSidebar()
        
    },
    toggleRegisterModal(){
            this.showLoginModal = false;
            this.showRegisterModal = !this.showRegisterModal;
            this.closeSidebar()
    },


    toggleForgotPasswordModal(){
        this.showLoginModal = false;
        this.showForgotPasswordModal = !this.showForgotPasswordModal;
        this.closeSidebar();
    },

    },

    computed:{
        isNavOpen(){
            return this.$store.getters.get_logged_status;
        },
        role(){
            return this.$store.getters.get_user_role;
        },
        logged_status(){
            return this.$store.getters.get_logged_status
        },
        profile_pic(){
            return this.$store.getters.get_user_profile_pic
        }
    },
    mounted(){
        const ioniconsEsmScript = document.createElement('script');
        ioniconsEsmScript.type = 'module';
        ioniconsEsmScript.src = 'https://unpkg.com/ionicons@7.1.0/dist/ionicons/ionicons.esm.js';
        document.head.appendChild(ioniconsEsmScript);

        const ioniconsScript = document.createElement('script');
        ioniconsScript.src = 'https://unpkg.com/ionicons@7.1.0/dist/ionicons/ionicons.js';
        document.head.appendChild(ioniconsScript);
    },

};

</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Montserrat&display=swap');

.main {
  max-width:100%;
  height: 100%;
  /* overflow: scroll; */
  /* padding:5vw; */
}

.logo {
    position: absolute;
    left: 20px;
    width: 100px;
    cursor: pointer;
}

li, a, button{
    font-family: "Montserrat", sans-serif;
    font-weight: 600;
    font-size: 16px;
    color: white;
    text-decoration: none;
    
}
header{
    /* background-color: #002423; */
    display: flex;
    justify-content: flex-end;
    align-items: center;
    box-shadow: 2px 2px 10px black;
}
header:hover{
    box-shadow: 2px 2px 25px black;
    transition: 0.5s;
}
ul.navlinks {
    display: flex;
    justify-content: center;
    align-items: center;
}
.navlinks li{
    /* display: inline-block;
    margin: 30px;
    align-items: center; */
    display: inline-block;
    padding: 1rem;
    margin-right: 10px;
}
.navlinks li.profile{
    margin-right: 10px;
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 0;
}

.profile-pic{
    height:40px;
    width:40px;
    border-radius: 50%;;
}
.navlinks.sidebar_active{
    margin:0;
}
.navlinks li a:hover{
    color: rgb(156 0 217);
    text-shadow: 1px 1px 5px black;
}

button{
    width: 100%;
    padding: 12px;
    background-color: firebrick;
    border-radius: 50px;
    outline: none;
    cursor: pointer;
    transition: all 0.5s, ease 0s;
    border: none;
    z-index: 999;
}
button:hover{
    box-shadow: 1px 1px 5px black;
}
.sidebar{
    position: fixed;
    top: 0;
    right: 0;
    height: 100vh;
    width: 300px;
    z-index: 999;
    background-color: transparent;
    backdrop-filter: blur(10px);
    box-shadow: -3px 0 10px black;
    display: none;
    justify-content: flex-start;
    list-style: none;
    flex-direction: column;
    transition: transform 0.3s ease;
    transform: translateX(100%);
}
.sidebar li{
    /* text-shadow: 1px 1px 2px black; */
    width: 100%;
    margin: 5px;
    padding: 1rem;
}

.items.active{
    background-color:#fff;
    color: var(--dark);
    border-radius: 50px;
    transition: background-color 1s ease-in-out;
}

.sidebar .active{
    background-color:#fff;
    color: var(--dark);
}


nav ion-icon{
    font-size: 2em;
    /* position: absolute; */
    top: 35px;
    right: 20px;
}
h2{ 
    color: wheat;
    text-shadow: #002423 -2px 2px 10px;
    font-size: 2em;
    margin: 20%;
    text-align: center;
}
@media only screen and (min-width: 830px){
    .navlinks ion-icon{
        display: none;
        
    }
}
@media only screen and (max-width: 830px){
    .navlinks .items{
        display: none;
    }
    .navlinks .profile{
        display: none !important;
    }
    .navlinks{
        margin:0;
    }
}
li{
    cursor: pointer;
}


</style>