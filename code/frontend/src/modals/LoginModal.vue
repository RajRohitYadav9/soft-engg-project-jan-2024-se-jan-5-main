<template>
    <div class="login-box" v-if="display">
        <span class="close-button" @click="$emit('close')">&times;</span>
        <form @submit.prevent="onSubmit">
        <div class="user-box">
          <input type="text" id="username" name="username" autocomplete="username" v-model="form.username" required>
          <label for="username">Username</label>
        </div>
        <div class="user-box">
          <input id="password" type="password" name="password" autocomplete="current-password" v-model="form.password" required>
          <label for="password">Password</label>
        </div>

        <div class="forgot-password">
          <label>Forgot Password </label>
          <span style="cursor: pointer;" @click="$emit('forgot_password')" class="material-symbols-outlined">
            arrow_circle_right
          </span>
          <!-- <input type="checkbox" @click="$emit('forgot_password')"> -->
        </div>
        <span v-if="msg != ''" class="error-message">{{ msg }}</span>
        <div class="center-button">
          <button type="submit">
                LOGIN
            <span></span>
          </button>
        </div>
      </form>
    </div>
  </template>
  
  <script>

import * as common from "../assets/common.js";


  export default {
    props: {
      display: Boolean,
    },
    emits: ["close", "forgot_password", "go_register" ],
    components :{
    },
    data(){
        return {
            form: {
                email: "",
                username: "",
                password: "",
            },
            msg:"",
        }
    },
    watch:{
      "form.username"(val){
        this.form.username = val;
        this.msg = ""
      },
      "form.password"(val){
        this.form.password = val;
        this.msg = ""
      }
    },

    methods: {
        onSubmit: async function (event) {
            event.preventDefault();
        //     const encoder = new TextEncoder();
        //     const decoder = new TextDecoder();
        //     const passwordBytes = encoder.encode(this.form.password);
        // //   this.$log.info("Submitting Login form");
        //     this.form.password = Base64.encode(passwordBytes);
            // this.form.password = btoa(this.form.password); // this btoa function is for legacy codes

            // this.form.password = this.form.password;

          const response = await fetch(common.AUTH_API_LOGIN, {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
            },
            body: JSON.stringify(this.form),
          })
          const data = await response.json();
          if (data.category == "success") {
                this.$flashMessage.successMessage('Successfully logged in');
                this.$emit("close");
                // update store
                this.$store.dispatch("set_state_after_login", data.message);
                this.$store.dispatch("token_timeout_fn", {});
                this.$router.push(`/${data.message.role}-home`); //home page depends on role
                // this.$router.push(`/student-home`); 
          }
          else{
                // this.form.password = decoder.decode(Base64.decode(this.form.password));
                this.msg = data.message;
                this.$flashMessage.failureMessage(data.message);
            }
        },

    },
};
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
  .error-message{
    margin:0;
    color:red;
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
label{
  color:#f2f2f2;
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
  background:none;
  border:none;
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

.forgot-password {
    display: flex;
    column-gap: 1rem;
}
  </style>
  