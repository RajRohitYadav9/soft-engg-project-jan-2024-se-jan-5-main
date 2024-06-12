
<template>
<LoadingAnimation v-show="loadingAnimation"></LoadingAnimation>
<div v-show="!loadingAnimation">
        <div class="ticket-thread">
        <!-- ticket 1 start -->
        <details open class="ticket" id="ticket-1">
            <a href="#ticket-1" class="ticket-border-link">
                <span class="sr-only">Jump to ticket-1</span>
            </a>
            <summary>
                <div class="ticket-heading">
                    <div class="ticket-info">
                        <a href="#" class="ticket-author">@{{ ticket.created_by }}</a>
                        <p class="m-0">
                            {{ ticket.votes }} votes &bull; {{ countDaysToDateTime(ticket.created_on) }}
                        </p>
                    </div>
                </div>
            </summary>

            <div class="ticket-body">
                <h1 style="font-size: var(--h1-text-size)">
                    {{ ticket.title }}
                </h1>
                <!-- <div v-html="markdown.render(ticket.description)"> -->
                <v-md-editor class="markdown" :model-value="ticket.description" mode="preview"></v-md-editor>
                <!-- </div> -->
                <div>
                <p>Attachments</p>
                    <div v-for="(attach, imageIndex) in ticket.ticket_attachments" :key="imageIndex">
                        <img :src="attach.attachment_loc" class="img-fluid" />
                    </div>
                </div>
                <div class="buttons">
                    <button type="button" v-if="owner" @click="toggleEditModal" >Edit</button>
                    <button type="button" v-if="owner" @click="toggleDeleteModal" >Delete</button>
                    <div v-if="support" class="custom-select">
                        <select @change="changePriority($event)" v-model="ticket.priority">
                            <option value="high">high</option>
                            <option value="low">low</option>
                            <option value="medium">medium</option>
                        </select>
                    </div>
                    <!-- <button type="button" v-if="support" @click="toggleChangePriorityModal" >{{ ticket.priority }}</button> -->
                    <!-- <button type="button" v-if="student_or_support" @click="toggleSolveStatus" >Mark As Solved</button> -->
                    <SolveButton v-if="owner_or_support && ticket.solution_id > 0" :solved="is_solved" :ticket_id="ticket.ticket_id"></SolveButton>

                    <LikeButton :ticket_id="ticket.ticket_id" type="button" v-if="!owner"></LikeButton>
                </div>

                <!-- Reply form start -->
                <form method="POST" class="reply-form d-none" id="ticket-1-reply-form">
                    <textarea placeholder="Reply to ticket" rows="4"></textarea>
                    <button type="submit">Submit</button>
                    <button type="button" data-toggle="reply-form" data-target="ticket-1-reply-form">Cancel</button>
                </form>
                <!-- Reply form end -->
            </div>

            <div v-if="ticket.solution_id != -1" class="replies">
                <!-- ticket 2 start -->
                <details open class="ticket" id="ticket-2">
                    <a href="#ticket-2" class="ticket-border-link">
                        <span class="sr-only">Jump to ticket-2</span>
                    </a>
                    <summary>
                    <div class="ticket-heading">
                        <div class="ticket-info">
                                <a href="#" class="ticket-author">@{{ ticket.resolved_by }}</a>
                                <p class="m-0">
                                    {{ countDaysToDateTime(ticket.resolved_on) }}
                                </p>
                            </div>
                        </div>
                    </summary>

                    <div class="ticket-body">
                        <!-- <div v-html="markdown.render(ticket.solution)"></div> -->

                        <v-md-editor class="markdown" :model-value="ticket.solution" mode="preview"></v-md-editor>
                        <!-- </div> -->
                        <div>
                        <p>Attachments</p>
                            <div v-for="(attach, imageIndex) in ticket.reply_attachments" :key="imageIndex">
                                <img :src="attach.attachment_loc" class="img-fluid" />
                            </div>
                        </div>
                    </div>
                </details>
            </div>
        </details>
        <!-- ticket 1 end -->
    </div>
    <div  >
        <ReplyButton v-if="ticket_reply_button" @click="toggleReplyModal" class="reply-button"></ReplyButton>
        <ReplyModal v-show="showReplyModal" :ticket_id="ticket.ticket_id" @replied="refresh()" @close="toggleReplyModal"></ReplyModal>
    </div>
    <EditModal :ticket="ticket" v-if="showEditModal" @ticketEdited="refresh()" @close="toggleEditModal" />
    <DeleteModal v-if="showDeleteModal" @delete="deleteTicket" @close="toggleDeleteModal" />

</div>
</template>

<script>
import LoadingAnimation from '../layouts/LoadingAnimation.vue';

import * as common  from "../assets/common"
import MarkdownIt from "markdown-it";


import { defineAsyncComponent } from "vue";

const markdown = new MarkdownIt();
export default {
    name: "TicketDetailsView",
    components: {
        LoadingAnimation,
        ReplyButton : defineAsyncComponent(() => import("../buttons/ReplyButton.vue")),
        LikeButton : defineAsyncComponent(() => import("../buttons/LikeButton.vue")),
        SolveButton: defineAsyncComponent(() => import("../buttons/SolveButton.vue")),
        ReplyModal: defineAsyncComponent(() => import("../modals/ReplyModal.vue")),
        EditModal: defineAsyncComponent(() => import("../modals/EditModal.vue")),
        DeleteModal: defineAsyncComponent(() => import("../modals/DeleteModal.vue"))
    },
    data(){
        return {
            ticket:{
                ticket_id: this.$route.params.ticket_id,
                title: "",
                description: "",
                priority: "low",
            },
            loadingAnimation : true,
            get_details_url: `${common.TICKET_API}/${this.$route.params.ticket_id}`,
            showReplyModal: false,
            markdown: markdown,
            showEditModal: false,
            showDeleteModal: false,
            showChangePriorityModal: false,
            
        }
    },
    methods: {

        async load(){
            try{
                const response = await fetch(this.get_details_url, {
                method: "GET",
                headers: {
                    "Content-Type": "application/json",
                    "Web-Token" : this.$store.getters.get_web_token,
                    "User-Id" : this.$store.getters.get_user_id,
                },
                })
                const data = await response.json()
                if (data.category == "success") {

                    this.ticket = data.message;

                }
                if (data.category == "error") {
                    this.$flashMessage.failureMessage(data.message);
                    this.$store.dispatch("set_state_after_logout");
                    this.$router.push("/");
                }

            }catch{

                this.$flashMessage.failureMessage("Internal Server Error");
            }
            return 0;
            
        },
        async refresh(){
            if(this.showEditModal){
                this.toggleEditModal();
            }
            if(this.showDeleteModal){
                this.toggleDeleteModal();
            }
            if(this.showReplyModal){
                this.toggleReplyModal();
            }
            this.loadingAnimation = true;
            await this.load();
            this.loadingAnimation = false;
            return 0;
        },
        async deleteTicket(){

            try{
                const response = await fetch(this.get_details_url, {
                        method: "DELETE",
                        headers: {
                        "Content-Type": "application/json",
                        "Web-Token" : this.$store.getters.get_web_token,
                        "User-Id" : this.$store.getters.get_user_id,
                        },
                    })
                const data = await response.json();
                if (data.category == "success") {
                    this.toggleDeleteModal();
                    this.$flashMessage.successMessage("Successfully Deleted a Ticket");
                    this.$router.push("/student-home");
                    
                }
                if (data.category == "error") {
                    this.toggleDeleteModal();
                    this.$flashMessage.failureMessage(data.message);
                    this.$store.dispatch("set_state_after_logout");
                    this.$router.push("/");
                }

            }catch{
                this.toggleDeleteModal();
                this.$flashMessage.failureMessage("Internal Server Error");
            }
            return 0;
        },
        countDaysToDateTime(value) {
                const today = new Date(); // Get today's date
                // const targetDatetime = new Date(value);
                var text = "";
                // Calculate the time difference in milliseconds (consider timezones if necessary)
                const timeDifference = today.getTime() - (value*1000);
                // Convert milliseconds to days (divide by 1000 milliseconds per second and 86400 seconds per day)
                const daysDifference = Math.floor(timeDifference / (1000 * 60 * 60 * 24));
                const hoursDifference = Math.floor(timeDifference / (1000 * 60 * 60));
                const minutesDifference = Math.floor(timeDifference / (1000 * 60));
                const secondsDifference = Math.floor(timeDifference / (1000));
                if (daysDifference > 0) {
                    text =  `${secondsDifference} ${secondsDifference === 1 ? 'day' : 'days'} ago`;
                } else if (hoursDifference > 0) {
                    text =  `${hoursDifference} ${hoursDifference === 1 ? 'hour' : 'hours'} ago`;
                } else if (minutesDifference > 0) {
                    text = `${minutesDifference} ${minutesDifference === 1 ? 'minute' : 'minutes'} ago`;
                } else {
                    text =  `${secondsDifference} ${secondsDifference === 1 ? 'second' : 'seconds'} ago`;
                }
            return text;
        },
        toggleReplyModal(){
            this.showReplyModal = !this.showReplyModal;
            setTimeout(() => {
                window.scrollTo(0, document.body.scrollHeight);
            }, 0);
        },
        toggleEditModal(){
            this.showEditModal = !this.showEditModal;
        },
        toggleDeleteModal(){
            this.showDeleteModal = !this.showDeleteModal;
        },
        toggleChangePriorityModal(){
            this.showChangePriorityModal = !this.showChangePriorityModal;
        },

        async changePriority(event){
            try{
                const response = await fetch(common.TICKET_API+"/change/priority",{
                            method: "POST",
                            headers: {
                                "Content-Type": "application/json",
                                "Web-Token" : this.$store.getters.get_web_token,
                                "User-Id" : this.$store.getters.get_user_id,
                            },
                            body: JSON.stringify({
                                "ticket_id" : this.ticket.ticket_id,
                                "priority" : event.target.value
                            })
                        })
                const data = await response.json();
                if (data.category == "success") {
                    this.$flashMessage.successMessage("Successfully Updated Priority");
                    
                }
                if (data.category == "error") {
                    this.refresh();
                    this.$flashMessage.failureMessage(data.message);
                }
            }catch{
                this.$flashMessage.failureMessage("Internal Server Error");
            }
            return 0;
        }

    },
    async mounted(){
        await this.load();
        this.loadingAnimation = false;
    },
    computed:{
        is_solved(){
            return this.ticket.status == 'resolved';
        },
        ticket_reply_button(){
            return this.ticket.status == 'pending' && (this.$store.getters.get_user_role  == "support" | this.$store.getters.get_user_role  == "admin") && !this.showReplyModal && this.ticket.status == "pending";
        },
        support(){
            return this.$store.getters.get_user_role == "support"
        },
        owner(){
            return this.$store.getters.get_user_id == this.ticket.owner_id;
        },
        owner_or_support(){
            return this.owner | this.support
        }
    },
}
</script>


<style scoped>

.reply-button {
    position: fixed;
    bottom: 10vh;
    right: 2vw;
}



.buttons{
    display: flex;
    margin-top: 1rem;
    margin-bottom: 1rem;
    flex-direction: row;
    column-gap: 10vw;
    justify-content: flex-start;
    align-items: center;
}

button {
    -moz-appearance: none;
    -webkit-appearance: none;
    appearance: none;
    font-size: 14px;
    padding: 4px 8px;
    color: rgba(0, 0, 0, 0.85);
    background-color: #fff;
    border: 1px solid rgba(0, 0, 0, 0.2);
    border-radius: 4px;
}
button:hover,
button:focus,
button:active {
    cursor: pointer;
    background-color: #ecf0f1;
}
.ticket-thread {
    max-width: 100%;
    margin: auto;
    padding: 0 30px;
    color: #f2f2f2;
    margin-bottom:10vh;
}
.m-0 {
    margin: 0;
    color:#f2f2f2;
}
.sr-only {
    position: absolute;
    left: -10000px;
    top: auto;
    width: 1px;
    height: 1px;
    overflow: hidden;
}

/* ticket */

.ticket {
    position: relative;
    margin: 20px auto;
}
.ticket-heading {
    display: flex;
    align-items: center;
    height: 50px;
    font-size: 14px;
}
.ticket-voting {
    width: 20px;
    height: 32px;
    border: 1px solid rgba(0, 0, 0, 0.2);
    border-radius: 4px;
}
.ticket-voting button {
    display: block;
    width: 100%;
    height: 50%;
    padding: 0;
    border: 0;
    font-size: 10px;
}
.ticket-info {
    color: rgba(0, 0, 0, 0.5);
    margin-left: 10px;
}
.ticket-author {
    color: rgb(156 0 217);
    text-decoration: none;
    font-size: 16px;
}
.ticket-author:hover {
    text-decoration: underline;
}
.replies {
    margin-left: 20px;
}

/* Adjustments for the ticket border links */

.ticket-border-link {
    display: block;
    position: absolute;
    top: 50px;
    left: 0;
    width: 12px;
    height: calc(100% - 50px);
    border-left: 4px solid transparent;
    border-right: 4px solid transparent;
    background-color: rgb(253 253 253 / 6%);
    background-clip: padding-box;
}
.ticket-border-link:hover {
    background-color: rgba(0, 0, 0, 0.3);
}
.ticket-body {
    padding: 0 20px;
    padding-left: 28px;
    overflow: scroll;
}
.replies {
    margin-left: 28px;
}

/* Adjustments for toggleable tickets */

details.ticket summary {
    position: relative;
    list-style: none;
    cursor: pointer;
}
details.ticket summary::-webkit-details-marker {
    display: none;
}
details.ticket:not([open]) .ticket-heading {
    border-bottom: 1px solid rgba(0, 0, 0, 0.2);
}
.ticket-heading::after {
    display: inline-block;
    position: absolute;
    right: 5px;
    align-self: center;
    font-size: 12px;
    color: rgba(0, 0, 0, 0.55);
}
details.ticket[open] .ticket-heading::after {
    content: "Click to hide";
    color: #f2f2f2;
}
details.ticket:not([open]) .ticket-heading::after {
    content: "Click to show";
    color: #f2f2f2;
}

/* Adjustment for Internet Explorer */

@media screen and (-ms-high-contrast: active), (-ms-high-contrast: none) {
    /* Resets cursor, and removes prompt text on Internet Explorer */
    .ticket-heading {
        cursor: default;
    }
    details.ticket[open] .ticket-heading::after,
    details.ticket:not([open]) .ticket-heading::after {
        content: " ";
    }
}

/* Styling the reply to ticket form */

.reply-form textarea {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif, "Apple Color Emoji", "Segoe UI Emoji", "Segoe UI Symbol";
    font-size: 16px;
    width: 100%;
    max-width: 100%;
    margin-top: 15px;
    margin-bottom: 5px;
}
.d-none {
    display: none;
}

.img-fluid {
  max-width: 100%;
  max-height: 500px;
  vertical-align: middle;
  border: 0;
}

.custom-select select{
    height: 32px;
}



/* solved button css */

/* The switch - the box around the slider */
.switch {
  font-size: 17px;
  position: relative;
  display: inline-block;
  width: 3.5em;
  height: 2em;
}

/* Hide default HTML checkbox */
.switch input {
  opacity: 0;
  width: 0;
  height: 0;
}

/* The slider */
.slider {
  position: absolute;
  cursor: pointer;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgb(182, 182, 182);
  transition: .4s;
  border-radius: 10px;
}

.slider:before {
  position: absolute;
  content: "";
  height: 1.4em;
  width: 1.4em;
  border-radius: 8px;
  left: 0.3em;
  bottom: 0.3em;
  transform: rotate(270deg);
  background-color: rgb(255, 255, 255);
  transition: .4s;
}

.switch input:checked + .slider {
  background-color: #21cc4c;
}

.switch input:focus + .slider {
  box-shadow: 0 0 1px #2196F3;
}

.switch input:checked + .slider:before {
  transform: translateX(1.5em);
}

</style>