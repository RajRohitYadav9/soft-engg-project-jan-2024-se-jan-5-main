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
                    <a href="#" class="ticket-author">@{{ faq.created_by }}</a>
                    <p class="m-0">
                        {{ 10 }} votes &bull; Official FAQ
                    </p>
                </div>
            </div>
        </summary>

        <div class="ticket-body">
            <h1 style="font-size: var(--h1-text-size)">
                {{ faq.question }}
            </h1>
            <v-md-editor class="markdown" :model-value="faq.solution" mode="preview"></v-md-editor>
            <div>
            <p>Attachments</p>
                <div v-for="(attach, imageIndex) in faq.attachments" :key="imageIndex">
                    <img :src="attach.attachment_loc" class="img-fluid" />
                </div>
            </div>
            <div class="buttons">
                <button type="button" v-if="admin" @click="toggleEditModal" >Edit</button>
                <button type="button" v-if="admin" @click="toggleDeleteModal" >Delete</button>
            </div>


        </div>

    </details>
    <!-- ticket 1 end -->
    </div>
    <FAQEditModal :faq="faq" v-if="showEditModal" @faqEdited="refresh()" @close="toggleEditModal" />
    <DeleteModal v-if="showDeleteModal" @delete="deleteFaq" @close="toggleDeleteModal" />
</div>
</template>

<script>
import MarkdownIt from "markdown-it";
import LoadingAnimation from '../layouts/LoadingAnimation.vue';

import { FAQ_API } from "../assets/common";
import { defineAsyncComponent } from 'vue';

const markdown = new MarkdownIt();
export default {
name: "FAQDetailsView",
components: {
    LoadingAnimation,
    FAQEditModal: defineAsyncComponent(()=> import('../modals/FAQEditModal.vue')),
    DeleteModal: defineAsyncComponent(()=> import('../modals/DeleteModal.vue'))
},
data(){
    return {
        markdown: markdown,
        loadingAnimation: true,
        showEditModal: false,
        showDeleteModal: false,
        faq : {}
    }
},
methods: {
    toggleEditModal(){
        this.showEditModal = !this.showEditModal;
    },
    toggleDeleteModal(){
        this.showDeleteModal = !this.showDeleteModal;
    },
    async load(){
            await fetch(FAQ_API+`/${this.$route.params.faq_id}`, {
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

                    this.faq = data.message;
                    
                }
                if (data.category == "error") {
                    this.$flashMessage.failureMessage(data.message);
                    this.$store.dispatch("set_state_after_logout");
                    this.$router.push("/");
                }
            })
            .catch(() => {
                this.$flashMessage.failureMessage("Internal Server Error");
            });
        },
        async deleteFaq(){
            await fetch(FAQ_API+`/${this.$route.params.faq_id}`, {
                method: "DELETE",
                headers: {
                    "Content-Type": "application/json",
                    "Web-Token" : this.$store.getters.get_web_token,
                    "User-Id" : this.$store.getters.get_user_id,
                },
            })
            .then((response) => response.json())
            .then((data) => {
                if (data.category == "success") {

                    this.$router.push("/faqs");
                }
                if (data.category == "error") {
                    this.$flashMessage.failureMessage(data.message);
                    this.$store.dispatch("set_state_after_logout");
                    this.$router.push("/");
                }
            })
            .catch(() => {
                this.$flashMessage.failureMessage("Internal Server Error");
            });
        },
        async refresh(){
            this.showEditModal = false;
            this.loadingAnimation = true;
            await this.load();
            this.loadingAnimation = false;
        }
},
computed:{
    admin(){
        return this.$store.getters.get_user_role == "admin"
    },
},

async mounted(){
    await this.load();
    this.loadingAnimation = false;

    
},
created(){

}

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
column-gap: 1rem;
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
height: auto;
vertical-align: middle;
border: 0;
}

</style>