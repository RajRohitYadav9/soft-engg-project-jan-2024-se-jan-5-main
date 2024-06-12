<template>
    <div class="toggle_buttons">
        <button :disabled="activeButton === 'Student'" @click="activateStudent" :class="{ 'disabled': activeButton === 'student' }">Student</button>
        <button :disabled="activeButton === 'Support'" @click="activateSupport" :class="{ 'disabled': activeButton === 'support' }">Support</button>
    </div>
    <div class="validate">
        <ValidateCard :remove=false @update="load()" v-for="user in needToValidateList" :key="user.user_id" :name="user.name" :email="user.email" :role="user.role" :userId="user.user_id"></ValidateCard>
    </div>
</template>

<script>
import ValidateCard from '../components/ValidateCard.vue';
import {show_error_and_logout} from '../utils/index';
import * as common from '../assets/common';

export default {
    components: {ValidateCard},
    data () {
        return {
            loadingAnimation: true,
            activeButton: "student",
            userList : [],
        }
    },
    methods:{
        async load(){
            await fetch(common.AUTH_API_NEWUSERS,{
            method: "GET",
            headers: {
            "Content-Type": "application/json",
            "Web-Token" : this.$store.getters.get_web_token,
            "User-Id" : this.$store.getters.get_user_id
            },
        })
        .then((response) => response.json())
        .then((data) => {
          if (data.category == "success") {
            this.userList = data.message;
          }
          if (data.category == "error") {
            show_error_and_logout(this,data.message);
          }
        })
        .catch(() => {
          this.$flashMessage.failureMessage("Internal Server Error");
        });
        return 0;
        },
        async activateStudent() {
            this.loadingAnimation = true
            await this.load()
            this.loadingAnimation = false
            this.activeButton = 'student';
        },
        async activateSupport() {
            this.loadingAnimation = true
            await this.load()
            this.loadingAnimation = false
            this.activeButton = 'support';
        }
    },

    computed:{
        needToValidateList(){
            if(this.userList.length > 0){
                return this.userList.filter(user => {
                    return user.role === this.activeButton;
                });
            }else{
                return []
            }
        }
    },
    created(){
        this.$store.dispatch("set_active_tab", "validate_users");
    },
    async mounted(){
        
        await this.load()
        this.loadingAnimation = false
    },
}
</script>

<style scoped>

.toggle_buttons{
    position: fixed;
    top: 14vh;
    right: 2vw;
    width: 200px;
    display: flex;
    flex-direction: row;
    justify-content: space-between;
    align-items: center;
    z-index: 100;
}

.toggle_buttons button{
    padding-left: 10px;
    padding-right: 10px;
    padding-top: 5px;
    padding-bottom: 5px;
    border: none;
    border-radius: 10px;
    background: #f2f2f2;
}

.validate{
    display: flex;
    margin-top: 16vh;
    justify-content: space-evenly;
    flex-wrap: wrap;
    align-items: center;
    row-gap: 1.5rem;
    column-gap:2rem;
}

button.student,button.support{
    background-color: white;
    color: black;
    border-radius: 10em;
    font-size: 17px;  
    font-weight: 600;
    padding: 1em 2em;
    cursor: pointer;
    transition: all 0.3s ease-in-out;
    border: 1px solid black;
    box-shadow: 0 0 0 0 black;
}
button.student,button.support:hover {
    transform: translateY(-4px) translateX(-2px);
    box-shadow: 2px 5px 0 0 black;
}

button.student,button.support:active {
    transform: translateY(2px) translateX(1px);
    box-shadow: 0 0 0 0 black;
}

button.disabled {
  background: grey;
  cursor: not-allowed;
}
</style>