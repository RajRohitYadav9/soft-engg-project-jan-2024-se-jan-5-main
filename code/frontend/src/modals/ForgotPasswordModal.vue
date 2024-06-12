<template>
    <div class="login-box" >
        <span class="close-button" @click="$emit('close')">&times;</span>
        <form @submit.prevent="onSubmit">
        <div class="user-box">
          <input type="text" id="username" name="username" autocomplete="username" v-model="username" required>
          <label for="username">Username</label>
        </div>
        <div v-if="!showSuccessMessage" class="center-button">
          <button type="submit">
                Get Password
            <span></span>
          </button>
        </div>
        <div v-else>
            {{ successMessage }}
        </div>
      </form>
    </div>
  </template>
  
  <script>
  import { FORGOT_PASSWORD_API } from '../assets/common';
  export default {
    emits: ["close"],
    data() {
      return {
        username: '',
        showSuccessMessage: false,
        successMessage: 'A new password has been successfully sent to your email address. You can now login with the new password.'
      }
    },
    methods: {
      async onSubmit() {

        try{
          const response = await fetch(FORGOT_PASSWORD_API+`/forgot/${this.username}`,{
            method:"POST",
            headers: {
              "Content-Type": "application/json",
            }
          })

          const data = await response.json();

          if(data.category == "success"){
            this.$flashMessage.successMessage(data.message);
            this.$emit("close");
          }else{
            this.$flashMessage.failureMessage(data.message);
          }
        }catch{
          this.$flashMessage.failureMessage("Internal Server Error, Try Later");
        }
      },
      closeMessage() {
        this.showSuccessMessage = false
        this.$emit("close");
      }
    }
  }
  </script>
  
  <style scoped>
  @media only screen and (min-width: 768px) { /* For screens wider than 768px */
        .login-box {
            margin: 0 auto;
            padding: 20px;
            min-width: 350px; /* Set a minimum width */
            max-width: 35%; /* Set a maximum width */
            border-radius: 10px; /* Add rounded corners */
            box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.2); /* Add subtle shadow */
            transition: 0.3s ease-in-out all; /* Add smooth transition */
    }
  }


  .close-button {
    color: #aaaaaa;
    float: right;
    font-size: 28px;
    font-weight: 200;
  }
  
  .close-button:hover,
  .close-button:focus {
    font-weight:800;
    text-decoration: none;
    cursor: pointer;
  }
  

  .modal-bottom{
    display:flex;
    flex-direction: row;
    justify-content: space-between;
    align-items:center;
    align-content: center;
    flex-wrap: wrap;
    font-size: var(--small-text-size);
  }
  p[type="msg"]{
    margin:0;
    margin-top:0.6rem;
  }
  /* a{
    text-decoration: none;
    color: var(--login-button-color);
  }  */

  form{
    margin-top:3rem;
  }


  /* God forgive me */
  .login-box {
  position: absolute;
  top: 50%;
  left: 50%;
  padding:20px;
  width:80%;
  transform: translate(-50%, -50%);
  background: rgba(24, 20, 20, 1);
  box-sizing: border-box;
  box-shadow: 0 15px 25px rgba(0,0,0,.6);
  border-radius: 10px;
  z-index:100;
}

.login-box .user-box {
  position: relative;
}

.login-box .user-box input {
  width: 100%;
  padding: 10px 0;
  font-size: 16px;
  color: #fff;
  margin-bottom: 30px;
  border: none;
  border-bottom: 1px solid #fff;
  outline: none;
  background: rgba(24, 20, 20, 1);
}

.login-box .user-box label {
  position: absolute;
  top: 0;
  left: 0;
  padding: 10px 0;
  font-size: 16px;
  color: #fff;
  pointer-events: none;
  transition: .5s;
}

.login-box .user-box input:focus ~ label,
.login-box .user-box input:valid ~ label {
  top: -20px;
  left: 0;
  color: #bdb8b8;
  font-size: 12px;
}

.login-box form button {
  position: relative;
  display: inline-block;
  padding: 10px 20px;
  color: #ffffff;
  font-size: 16px;
  text-decoration: none;
  text-transform: uppercase;
  overflow: hidden;
  transition: .5s;
  margin-top: 40px;
  letter-spacing: 4px;
  cursor: pointer;
  background: none;
  border: none;
}

.login-box button:hover {
  background: #f2f2f2;
  color: #000000;
  border-radius: 5px;
}

.login-box button span {
  position: absolute;
  display: block;
}

@keyframes btn-anim1 {
  0% {
    left: -100%;
  }

  50%,100% {
    left: 100%;
  }
}

.login-box button span:nth-child(1) {
  bottom: 2px;
  left: -100%;
  width: 100%;
  height: 2px;
  background: linear-gradient(90deg, transparent, #f2f2f2);
  animation: btn-anim1 2s linear infinite;
}

.center-button {
    text-align: center;
}
  </style>
  