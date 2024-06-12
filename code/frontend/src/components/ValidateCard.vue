<template>
    <div class="card">
    <div class="top-section">
      <div class="border"></div>
      <div class="icons">
        OSTS
      </div>
      <div class="details">
        <span class="name">{{ name }}</span>
        <span class="email">{{ email }}</span>
      </div>
    </div>
    <div class="bottom-section">
      <span class="title">{{role}}</span>
      <div class="row row1">
        <div v-if="!remove" class="item-1">
          <span @click="accept()" class="material-symbols-outlined button">done</span>
        </div>
        <div class="item-0">
          <span class="big-text"></span>
          <span class="regular-text"></span>
        </div>
        <div class="item-1">
          <span v-if="!remove" class="button material-symbols-outlined" @click="reject()" >close</span>
        </div>
        <div class="item-2">
          <span v-if="remove" class="button material-symbols-outlined" @click="removeUser()" >delete</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script>

import { AUTH_API_NEWUSERS, USER_API } from '../assets/common';
import {show_error_and_logout} from '../utils/index';



export default{
    name : "ValidateCard",
    props: {"name":String, "email": String, "role": String, "userId": String , "remove": Boolean},
    emits: ["update","deleted"],
    data(){
      return {
          user_id : this.userId
      }
    },
    methods:{
      accept(){
        fetch(AUTH_API_NEWUSERS + `/${this.user_id}`, {
          method: "PUT",
          headers: {
          "Content-Type": "application/json",
          "Web-Token" : this.$store.getters.get_web_token,
          "User-Id" : this.$store.getters.get_user_id,
          },
          body: JSON.stringify({"user_id": this.user_id})
        })
        .then((response) => response.json())
        .then((data) => {
          if (data.category == "success") {

            this.$flashMessage.successMessage("Successfully Verified")
            this.$emit("update")
          }
          if (data.category == "error") {
            show_error_and_logout(this,data.message);
          }
        })

      },
      reject(){
        fetch(AUTH_API_NEWUSERS + `/${this.user_id}`, {
          method: "DELETE",
          headers: {
          "Content-Type": "application/json",
          "Web-Token" : this.$store.getters.get_web_token,
          "User-Id" : this.$store.getters.get_user_id,
          },
          body: JSON.stringify({"user_id": this.user_id})
        })
        .then((response) => response.json())
        .then((data) => {
          if (data.category == "success") {

            this.$flashMessage.successMessage("Successfully Rejected")
            this.$emit("update")
          }
          if (data.category == "error") {
            show_error_and_logout(this,data.message);
          }
        })

      },
      removeUser(){
        fetch(USER_API + `/${this.user_id}`, {
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

            this.$flashMessage.successMessage("Successfully Deleted")
            this.$emit("deleted")
          }
          if (data.category == "error") {
            show_error_and_logout(this,data.message);
          }
        })
      }
    }
}
</script>

<style scoped>

.card {
  width: 230px;
  border-radius: 20px;
  background: var(--card-background-color);
  padding: 5px;
  overflow: hidden;
  /* box-shadow: rgba(100, 100, 111, 0.2) 0px 7px 20px 0px; */
  transition: transform 0.5s cubic-bezier(0.175, 0.885, 0.32, 1.275);
}

.card:hover {
  transform: scale(1.05);
}

.card .top-section {
  height: 100px;
  border-radius: 15px;
  display: flex;
  flex-direction: column;
  background: linear-gradient(45deg, rgb(35 35 35) 0%, rgb(0 0 0 / 55%) 100%);
  position: relative;
}

.card .top-section .border {
  border-bottom-right-radius: 10px;
  height: 30px;
  width: 130px;
  background: var(--card-background-color);
  position: relative;
  transform: skew(-40deg);
  box-shadow: -10px -10px 0 0 var(--card-background-color);
}

.card .top-section .border::before {
  content: "";
  position: absolute;
  width: 15px;
  height: 15px;
  top: 0;
  right: -15px;
  background: rgba(255, 255, 255, 0);
  border-top-left-radius: 10px;
  box-shadow: -5px -5px 0 2px var(--card-background-color);
}

.card .top-section::before {
  content: "";
  position: absolute;
  top: 30px;
  left: 0;
  background: rgba(255, 255, 255, 0);
  height: 15px;
  width: 15px;
  border-top-left-radius: 15px;
  box-shadow: -5px -5px 0 2px var(--card-background-color);
}

.card .top-section .icons {
  position: absolute;
  top: 0.2rem;
  right: 0.5rem;
  color:white;
  font-weight: bold;
  letter-spacing: 2px;
}

.card .top-section .icons .logo {
  /* height: 100%;
  aspect-ratio: 1;
  padding: 7px 0 7px 15px; */
  display: flex;
  justify-content: flex-end;
  align-items: center;
  /* width: min-content; */
  position: relative;
  top: -1.5rem;
  right: 2rem;
}

.card .top-section .icons .logo .top-section {
  height: 100%;
}

.details{
    display: flex;
    color:white;
    flex-direction: column;
    justify-content: space-between;
    align-items: center;
    row-gap: 0.8rem;
    margin-top: 0.5rem;
}


.card .bottom-section {
  margin-top: 15px;
  padding: 10px 5px;
}

.card .bottom-section .title {
  display: block;
  font-size: 17px;
  font-weight: bolder;
  color: white;
  text-align: center;
  letter-spacing: 2px;
}

.card .bottom-section .row {
  display: flex;
  justify-content: space-between;
  margin-top: 20px;
}


.card .bottom-section .row .item .big-text {
  font-size: 12px;
  display: block;
}

.card .bottom-section .row .item .regular-text {
  font-size: 9px;
}

.card .bottom-section .row .item:nth-child(2) {
  border-left: 1px solid rgba(255, 255, 255, 0.126);
  border-right: 1px solid rgba(255, 255, 255, 0.126);
}

.item-1,.item-0{
  flex: 30%;
  text-align: center;
  color:white;
  padding: 5px;
}

.item-2{
  text-align: center;
  padding: 5px;
  color:white;
}

.item-1, .item-2{
  cursor:pointer;
}

</style>