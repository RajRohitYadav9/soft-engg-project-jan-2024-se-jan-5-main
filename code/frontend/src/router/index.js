
import {createRouter,createWebHistory} from 'vue-router';
import LoginView from '../views/LoginView.vue';
// import CreateAccountView from '@/views/CreateAccountView.vue';
// import RegisterView from '../views/RegisterView.vue';
import store from '../store';
import * as common from "../assets/common.js";
// import StudentCreateTicket from '../views/StudentCreateTicket.vue';
// import StudentMyTickets from '../views/StudentMyTickets.vue';
// import SupportMyTickets from '../views/SupportMyTickets.vue';
// import AdminCreateFAQ from '../views/AdminCreateFAQ.vue';

import AppHomeView from '../views/AppHomeView.vue';

// import UserProfile from '../views/UserProfile.vue';

// experimental features
import reply from '../experimental/reply.vue'


const routes = [
  {
    path: '/',
    alias: '/home',
    name: 'AppHomeView',
    component: AppHomeView,
    meta: {disallowAuthed: true},
    beforeEnter: (to, from, next) => {  
      // Your guard logic here
      const role = store.state.user.role;
      const isAuthenticated = store.getters.get_logged_status;
      // For example, check if user is authenticated
      if (isAuthenticated) {
        return next(`/${role}-home`);
      } 
      // else {
      //   return next('/'); // Redirect to login page
      // }
      next();
    }
  },
  {
    path: '/login',
    name: 'LoginView',
    component: LoginView,
  },
//   {
//     path: '/register',
//     name: 'RegisterView',
//     component: RegisterView,
//   },
  {
    path: '/student-home',
    name: 'StudentHome',
    component: () => import('../views/StudentHome.vue'),
  },
  {
    path: '/student-activity',
    name: 'StudentActivity',
    component: () => import('../views/StudentActivity.vue'),
  },
  {
    path: '/all-tickets',
    name: 'AllTicketView',
    component: () => import('../views/AllTicketView.vue'),
  },
  {
    path: '/ticket/:ticket_id',
    name: 'TicketDetailsView',
    component : () => import('../views/TicketDetailsView.vue'),
  },
  {
    path: '/onlyview/:ticket_id',
    name: 'TicketRestrictedDetails',
    component : () => import('../views/TicketRestrictedDetails.vue'),
  },

//   {
//     path: '/student-create-ticket',
//     name: 'StudentCreateTicket',
//     component: StudentCreateTicket,
//   },
//   {
//     path: '/student-my-tickets',
//     name: 'StudentMyTickets',
//     component: StudentMyTickets,
//   },
//   {
//     path: '/user-profile',
//     name: 'UserProfile',
//     component: UserProfile,
//   },
  {
    path: '/support-home',
    name: 'SupportHome',
    component: () => import('../views/AllTicketView.vue'),
  },
  {
    path: '/support-activity',
    name: 'SupportActivity',
    component: () => import('../views/SupportActivity.vue'),
  },
//   {
//     path: '/support-my-tickets',
//     name: 'SupportMyTickets',
//     component: SupportMyTickets,
//   },
  {
    path: '/admin-home',
    name: 'AdminHome',
    component: () => import('../views/AdminHome.vue'),
  },
  {
    path: '/reply',
    name: 'reply',
    component: reply,
  },
  {
    path: '/faqs',
    name: 'CommonFAQs',
    component: () => import('../views/CommonFAQs.vue'),
  },
  {
    path: '/faq/:faq_id',
    name: 'FAQDetailsView',
    component: () => import('../views/FAQDetailsView.vue'),
  },
  {
    path: '/admin-validate-users',
    name: 'AdminValidateUsers',
    component: () => import('../views/AdminValidateUsers.vue'),
  },
  {
    path: '/admin/manage',
    name: 'AdminManage',
    component: () => import('../views/AdminManage.vue'),
  },
  {
    path: '/profile',
    name: 'ProfilePage',
    component: () => import("../views/ProfilePage.vue")
  },
];

export const router = createRouter({

  history: createWebHistory(),
  base: process.env.BASE_URL,
  routes, // short for `routes: routes`
})

router.beforeEach((to, from, next) => {
  // redirect to login page if not logged in and trying to access a restricted page
  const publicPages = ['/login', '/register', '/', '/home', '/reply', '/faqs', '/onlyview/:ticket_id'];
  const authRequired = !publicPages.includes(to.matched[0].path);
  if (!store.getters.get_logged_status) {
    store.commit('initialiseStore');
    // store.dispatch('initialiseStore');
  }
  const logged_status = store.getters.get_logged_status;


  if (authRequired && !logged_status) {
    alert("Token expired. Please log in again.");
    return next('/');
  }

  if (authRequired && logged_status) {
    const role = store.getters.get_user_role;
    var path_str="";
    var matched="";
    if(to.matched.path != "/"){
      path_str = to.matched[0].path.split("/");
      matched = "/"+path_str[1];
    }else{
      matched = "/";
    }
    if (((role === 'student') && (common.STUDENT_ROUTES.includes(matched)))
      || ((role === 'support') && (common.SUPPORT_ROUTES.includes(matched)))
      || ((role === 'admin') && (common.ADMIN_ROUTES.includes(matched)))) {
      return next();
    }
    else {
      alert("You don't have access to this page.");
      return next(`/${role}-home`);
    }
  }
  
  next();
})

export default router;
