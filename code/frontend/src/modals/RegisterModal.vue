<template>
    <div class="modal" v-if="display">
      <div class="modal-content">
        <span class="close-button" @click="$emit('close')">&times;</span>
        <h1 class="modal-heading">Create An Account</h1>
        <form @submit.prevent="onSubmit">
            <label for="name">Name</label>
            <input id="name" name="name" v-model="form.name" placeholder="name" required/>
            <label for="username">Username</label>
            <input id="username" name="username" v-model="form.username" placeholder="username" required/>
            <label for="role_selection">Select Role</label>
            <select v-model="form.role" class="role_selection">
                <option value="student">Student</option>
                <option value="support">Support</option>
                <!-- <option value="admin">Admin</option> -->
                </select>
            <label for="email">Email</label>
            <input type="email" id="email" name="email" v-model="form.email" placeholder="Enter email" required/>
            <label for="password">Password</label>
            <input type="password" id="password" name="password" v-model="form.password" placeholder="Enter password" required />
            <!-- <span v-if="errors.formatPassword" class="error-message" >{{ errors.passwordFormatMessage }}</span> -->
            <label for="confirm_password">Confirm Password</label>
            <input type="password" id="confirm_password" name="confirm_password" v-model="form.retype_password" placeholder="Retype password" required  />
            <!-- <span v-if="errors.retypePassword" class="error-message" >{{ errors.retypePasswordMessage }}</span> -->
            <span v-if="msg != ''" class="error-message">{{ msg }}</span>
            <div class="button-div">
              <div>
                <button type="submit" >Create
                  <span></span>
                </button>
                
              </div>

                <div>
                  <button  type="reset" @click="onReset" >Reset
                    <span></span>
                  </button>
                  
              </div>
                
            </div>

        </form>
      </div>
    </div>
  </template>
  
  <script>
// import { ref } from 'vue';
import * as common from "../assets/common.js";

// import { Base64 } from 'js-base64';  //installed js-base64

  export default {
    props: {
      display: Boolean,
    },
    data(){
        return {
            role_options: "student",
            form: {
                name: "",
                username: "",
                role: "student",
                email: "",
                password: "",
                retype_password: "",
            },
            msg:"",
            show: true,
            errors:{
                any: false,
                formatPassword: false,
                retypePassword: false,
                passwordFormatMessage: "Password should contain letters A-Z a-z and numbers 0-9 only and should be atleast 4 and atmost 8 characters long.",
                retypePasswordMessage: "Password did not match."
            }
        }
    },
    watch:{
      'form.email'(value){
        // binding this to the data value in the email input
        this.form.email = value;
        this.validateEmail(value);
        },
      'form.password'(value){
          this.form.password = value;
          this.validatePassword(value);
        },
      'form.retype_password'(value){
          this.form.retype_password = value;
          this.validateRetypePassword(value);
        },
      'form.username'(value){
          this.form.username = value;
          this.validateUsername(value);
        }
    },
    methods: {
      onSubmit(event) {
        if(!this.has_error_msg){

          event.preventDefault();
        //   alert('You are creating a new account. Click "Ok" to proceed?');
        //   this.$log.info("Submitting Registration form");

          // const encoder = new TextEncoder();

          // this.form.password = Base64.encode(encoder.encode(this.form.password));
          // this.form.retype_password = Base64.encode(encoder.encode(this.form.retype_password));

          fetch(common.AUTH_API_REGISTER, {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
            },
            body: JSON.stringify(this.form),
          })
            .then((response) => response.json())
            .then((data) => {
              if (data.category == "success") {
                this.$flashMessage.successMessage(data.message);
                this.onReset()
                this.$emit("reg_success");
              }
              if (data.category == "error") {
                this.$flashMessage.failureMessage(data.message);
              }
            })
            .catch(() => {
              // this.$log.error(`Error : ${error}`);
              this.$flashMessage.failureMessage("Internal Server Error",);
            });
          }
    },
    onReset() {
      this.form.name = "";
      this.form.username = "";
      this.form.email = "";
      this.form.password = "";
      this.form.retype_password = "";
      // Trick to reset/clear native browser form validation state
      this.show = false;
      this.$nextTick(() => {
        this.show = true;
      });
    },
    check_password() {
      let password = this.form.password;
      if (password.length < 4 || password.length > 9) {
        this.errors.formatPassword = true;
        this.errors.any = true;
        return false;
      }
      const valid_char_array = Array.from(
        "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
      );
      const password_array = Array.from(password);
      for (let i = 0; i < password_array.length; i++) {
        if (!valid_char_array.includes(password_array[i])) {
            this.errors.formatPassword = true;
            this.errors.any = true;
            
          return false;
        }
      }

      this.errors.formatPassword = false;
      this.errors.any = false;
      return true;
    },
    check_retype_password() {
      if(this.form.password === this.form.retype_password){
        this.errors.any = false;
        this.errors.retypePassword = false;
        return false;
      }else{
        this.errors.any = true;
        this.errors.retypePassword = true;
        return true;
      }
    },

    validateEmail(value){
        if (/^\w+([.-]?\w+)*@\w+([.-]?\w+)*(\.\w{2,3})+$/.test(value)){
            this.msg = '';
            }
            else{
            this.msg = 'Invalid Email Address';
        } 
    },
        
    validatePassword(value){
          let difference = 8 - value.length;
          if (value.length<8) {
            this.msg = 'Password must be 8 characters! '+ difference + ' characters left' ;
          } else {
            this.msg = '';
          }
      },
    validateRetypePassword(value){
      if(value.length >= 8){
          if (value != this.form.password) {
            this.msg = 'Password is not matching' ;
          } else {
            this.msg = '';
          }
      }
    },
    validateUsername(username) {
      const usernameRegex = /^[a-zA-Z0-9_]+$/;
      if (usernameRegex.test(username)){
          this.msg = "";
      }else{
        this.msg = "No Special Character is allowed"
      }
    }
  },
  computed: {
    check_name() {
      return this.form.name.length > 2 ? true : false;
    },
    has_error_msg(){
      return this.msg != "";
    }

  },
};
  </script>
  
  <style scoped>
  @media only screen and (min-width: 768px) { /* For screens wider than 768px */
        .modal-content {
            margin: 0 auto;
            background: rgba(24, 20, 20, 1);
            padding: 20px;
            min-width: 350px; /* Set a minimum width */
            max-width: 35%; /* Set a maximum width */
            border-radius: 10px; /* Add rounded corners */
            box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.2); /* Add subtle shadow */
            transition: 0.3s ease-in-out all; /* Add smooth transition */
    }
    input{
        margin-bottom: 30px;
    }
  }
  
  .modal {
    position: fixed; /* Stay in place */
    z-index: 1; /* Sit on top */
    left: 0;
    top: 0;
    width: 100%; /* Full width */
    height: 100%; /* Full height */
    overflow: auto; /* Enable scroll if needed */
    background-color: rgba(0, 0, 0, 0.4); /* Black w/ opacity */
    transition: 0.3s ease-in-out all; /* Add smooth transition */
  }
  
  .modal-content {
    background: rgba(24, 20, 20, 1);
    color: #fff;
    margin: 0 auto; /* 15% from the top and centered */
    padding: 20px;
    width:80%;
    border-radius: 10px; /* Add rounded corners */
    box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.2); /* Add subtle shadow */
    transition: 0.3s ease-in-out all; /* Add smooth transition */
    position: absolute;
    top: 50%;
    left:50%;
    transform: translate(-50%, -50%);
  }
  
  .close-button {
    color: #aaaaaa;
    float: right;
    font-size: 28px;
    font-weight: 200;
  }
  
  .close-button:hover,
  .close-button:focus {
    font-weight: 800;
    text-decoration: none;
    cursor: pointer;
  }
  
  .modal-heading {
    text-align: center;
    font-size: large;
  }
  
  form {
    display: flex;
    flex-direction: column;
    /* align-items: center; */
  }
  
  label {
    margin-bottom: 5px;
    margin-top: 5px;
  }
  
  .role_selection, 
  input {
    /* width: 100%;
    padding: 12px 20px;
    margin: 8px 0;
    display: inline-block;
    border: 1px solid #ccc;
    border-radius: 4px;
    box-sizing: border-box; */
    width: 100%;
  padding: 10px 0;
  font-size: 16px;
  color: #fff;
  /* margin-bottom: 30px; */
  border: none;
  border-bottom: 1px solid #fff;
  outline: none;
  background: rgba(24, 20, 20, 1);
  }

  .button-div{
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 5rem;
  }
  
  button[type="submit"], button[type="reset"] {
    /* max-width:25%;
    background-color: var(--login-button-color);
    color: white;
    padding: 10px 20px;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    font-size: var(--medium-text-size);
    transition: 0.3s ease-in-out background-color; */

    display: inline-block;
  color: #ffff;
  padding: 10px 20px;
  background-color: transparent;
  font-size: 16px;
  border: none;
    border-radius: 4px;
    cursor: pointer;
  text-decoration: none;
  text-transform: uppercase;
  overflow: hidden;
  transition: .5s;
  letter-spacing: 3px;
  background: none;
  border: none;
  }
  
  button[type="submit"]:hover, button[type="reset"]:hover {
    background-color: var(--login-button-hover-color); /* Change background color on hover */
    background: #f2f2f2;
    color: #000000;
    font-weight: 500;
    border-radius: 5px;

  }

  .error-message{
    color: red;
    font-size: var(--smallest-text-size);
  }
  button span {
  position: relative;
  display: block;
}


  @keyframes btn-anim1 {
  0% {
    left: -100%;
  }

  50%,100% {
    left: 130%;
  }
}

button span:nth-child(1) {
  left: -100%;
  width: 100%;
  height: 2px;
  background: linear-gradient(90deg, transparent, #f2f2f2);
  animation: btn-anim1 2s linear infinite;
}
  </style>
  