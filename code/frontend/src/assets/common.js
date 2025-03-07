/* eslint-disable */

const BASEURL = "http://127.0.0.1:5000";
const VERSION = "v1";

const AUTH_API_PREFIX = `/api/${VERSION}/auth`;
const STUDENT_API_PREFIX = `/api/${VERSION}/student`;
const SUPPORT_API_PREFIX = `/api/${VERSION}/support`;
const ADMIN_API_PREFIX = `/api/${VERSION}/admin`;
const FAQ_API_PREFIX = `/api/${VERSION}/faq`;
const TICKET_API_PREFIX = `/api/${VERSION}/ticket`;
const USER_API_PREFIX = `/api/${VERSION}/user`;
const TICKET_API_CREATE_PREFIX = `/api/${VERSION}/ticket/create`;
const AUTH_API_LOGIN = `${BASEURL}${AUTH_API_PREFIX}/login`;
const AUTH_API_REGISTER = `${BASEURL}${AUTH_API_PREFIX}/register`;
const AUTH_API_NEWUSERS = `${BASEURL}${AUTH_API_PREFIX}/newUsers`;
const USER_API = `${BASEURL}${USER_API_PREFIX}`

const STUDENT_API = `${BASEURL}${STUDENT_API_PREFIX}`;
const SUPPORT_API = `${BASEURL}${SUPPORT_API_PREFIX}`;
const ADMIN_API = `${BASEURL}${ADMIN_API_PREFIX}`;
const FAQ_API = `${BASEURL}${FAQ_API_PREFIX}`;
const TICKET_API = `${BASEURL}${TICKET_API_PREFIX}`;
const TICKET_API_CREATE = `${BASEURL}${TICKET_API_CREATE_PREFIX}`;
const TICKET_TAGS_API = `${TICKET_API}/tags`
const TICKET_REPLY = `${TICKET_API}/reply`
const FORGOT_PASSWORD_API = `${BASEURL}/api/${VERSION}/password`

const TICKET_API_ALLTICKETS = `${BASEURL}${TICKET_API_PREFIX}/all-tickets`

const FEW_TICKETS = `${BASEURL}${TICKET_API_PREFIX}/few-tickets`


const STUDENT_ROUTES = ['/student-activity', '/student-home', "/student-create-ticket", "/student-my-tickets", "/faq", "/user-profile", "/all-tickets", "/ticket", "/profile"]
const SUPPORT_ROUTES = ['/support-activity', '/support-home', "/support-my-tickets", "/faq", "/user-profile", "/ticket", "/profile"]
const ADMIN_ROUTES = ['/admin', '/admin-home', "/admin-create-faq", "/admin-validate-users", "/all-tickets", "/faq", "/user-profile", "/ticket", "/admin/manage", "/profile"]

const STUDENT_NAV_BUTTONS = [
  { id: 1, title: "Home", link: "/student-home", active: false },
  { id: 2, title: "Create Ticket", link: "/student-create-ticket", active: false },
  { id: 3, title: "My Tickets", link: "/student-my-tickets", active: false },
  { id: 4, title: "FAQs", link: "/common-faqs", active: false },
  { id: 5, title: "Logout", link: "#", active: false },
]

const SUPPORT_NAV_BUTTONS = [
  { id: 1, title: "Home", link: "/support-home", active: false },
  { id: 2, title: "My Tickets", link: "/support-my-tickets", active: false },
  { id: 3, title: "FAQs", link: "/common-faqs", active: false },
  { id: 4, title: "Logout", link: "#", active: false },
]

const ADMIN_NAV_BUTTONS = [
  { id: 1, title: "Home", link: "/admin-home", active: false },
  { id: 2, title: "Validate Users", link: "/admin-validate-users", active: false },
  { id: 3, title: "Create FAQ", link: "/admin-create-faq", active: false },
  { id: 4, title: "FAQs", link: "/common-faqs", active: false },
  { id: 5, title: "Logout", link: "#", active: false },
]

export {
  AUTH_API_LOGIN,
  AUTH_API_REGISTER,
  AUTH_API_NEWUSERS,
  STUDENT_API_PREFIX,
  SUPPORT_API_PREFIX,
  ADMIN_API_PREFIX,
  FAQ_API_PREFIX,
  TICKET_API_ALLTICKETS,
  FEW_TICKETS,
  TICKET_API_PREFIX,
  TICKET_API_CREATE_PREFIX,
  TICKET_API_CREATE,
  STUDENT_API,
  SUPPORT_API,
  ADMIN_API,
  FAQ_API,
  USER_API,
  FORGOT_PASSWORD_API,
  TICKET_API,
  TICKET_REPLY,
  TICKET_TAGS_API,
  STUDENT_ROUTES,
  SUPPORT_ROUTES,
  ADMIN_ROUTES,
  STUDENT_NAV_BUTTONS,
  SUPPORT_NAV_BUTTONS,
  ADMIN_NAV_BUTTONS
};
