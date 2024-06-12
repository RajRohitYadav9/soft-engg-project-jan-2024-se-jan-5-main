<template>
    <LoadingAnimation v-show="loadingAnimation"></LoadingAnimation>
    <div v-show="!loadingAnimation">
    <div class="profile-page">
      <h2>Profile</h2>
      <div class="profile-info">
        <div class="profile-picture-container">
          <img :src="user.profilePicture" alt="Profile Picture" />
        </div>
        <div class="user-details">
          <p>Username: {{ user.username }}</p>
          <p>Email: {{ user.email }}</p>
        </div>
      </div>
      <div class="profile-actions">
        <h3 for="upload-pic">Update Profile Picture</h3>
        <input id="upload-pic" name="upload-pic" type="file" ref="pictureInput" @change="handleImage" />
        <button class="update-profile-pic" @click="updatePicture" >Update</button>
        <div class="change-password">
            <h3>Change Password</h3>
            <form @submit.prevent="changePassword">
              <label for="currentPassword">Current Password</label>
              <input type="password" id="currentPassword" v-model="currentPassword" required />
              <label for="newPassword">New Password</label>
              <input type="password" id="newPassword" v-model="newPassword" required />
              <label for="confirmPassword">Confirm New Password</label>
              <input type="password" id="confirmPassword" v-model="confirmPassword" required />
              <span v-if="msg != ''" class="error-message">{{ msg }}</span>
              <button type="submit">Change Password</button>
            </form>
        </div>
      </div>
    </div>
  </div>
  </template>
  
  <script>
import LoadingAnimation from '../layouts/LoadingAnimation.vue';
import {USER_API} from '../assets/common';

  export default {
    components:{LoadingAnimation},
    data() {
      return {
        loadingAnimation: true,
        user: {
          username: "",
          email: "",
          profilePicture: "",
        },
        msg:"",
        currentPassword: "",
        newPassword: "",
        confirmPassword: "",
        form:{
          profile_photo_loc : null,
        },
      };

    },
    watch: {
      currentPassword(value){
          this.currentPassword = value;
          this.validatePassword(value);
        },
      newPassword(value){
          this.newPassword = value;
          this.validatePassword(value);
        },
      confirmPassword(value){
          this.confirmPassword = value;
          this.validateRetypePassword(value);
        },
    },
    created() {
      // Fetch user data from your backend
      // Replace with your actual logic
      this.$store.dispatch("set_active_tab", "profile");

    },
    mounted(){
      this.user = {
        username: this.$store.getters.get_username,
        email: this.$store.getters.get_email,
        profilePicture: this.$store.getters.get_user_profile_pic,
      };
      this.loadingAnimation = false;
    },
    methods: {
      async handleImage(event){
        const file = await event.target.files[0];

        const base64 =  await this.fileToBase64(file);
  
        this.form.profile_photo_loc = base64;
        this.user.profilePicture = URL.createObjectURL(file);
      },
      fileToBase64(file) {
        return new Promise((resolve, reject) => {
          const reader = new FileReader();
          reader.readAsDataURL(file);
          reader.onload = () => resolve(reader.result);
          reader.onerror = (error) => reject(error);
        });
      },
      async updatePicture() {
        try{
            let resp = await fetch(USER_API+"/profile",{
                          method: "PUT",
                          headers: {
                            "Content-Type": "application/json",
                            "Web-Token": this.$store.getters.get_web_token,
                            "User-Id": this.$store.getters.get_user_id,
                          },
                          body: JSON.stringify(this.form)
                        });

            const data = await resp.json();
                if (data.category == "success") {
                    this.$flashMessage.successMessage("Successfully Uploaded Profilr Picture");      
                    this.$store.dispatch("set_state_after_profile_pic_update", this.form)
                }
                if (data.category == "error") {
                    this.$flashMessage.failureMessage(data.message);
                }
             // Temporary URL for preview
        }catch{
          this.$flashMessage.failureMessage("Internal Server Error");
        }
        return 0;
      },
      async changePassword() {
          if (this.msg == "") {

            try{
                  let resp = await fetch(USER_API+"/profile",{
                                method: "PUT",
                                headers: {
                                  "Content-Type": "application/json",
                                  "Web-Token": this.$store.getters.get_web_token,
                                  "User-Id": this.$store.getters.get_user_id,
                                },
                                body: JSON.stringify({
                                  "previous_password": this.currentPassword,
                                  "new_password": this.newPassword,
                                })
                              });
                  const data = await resp.json();
                      if (data.category == "success") {
                          this.$flashMessage.successMessage("Successfully Changed Password");      
                      }
                      if (data.category == "error") {
                          this.$flashMessage.failureMessage(data.message);
                      }
                  // Temporary URL for preview
              }catch{
                this.$flashMessage.failureMessage("Internal Server Error");
              }

          }
          return 0;
      },
      validatePassword(value){
          let difference = 8 - value.length;
          if (value.length<8) {
            this.msg = 'Must be 8 characters! '+ difference + ' characters left' ;
          } else {
            this.msg = '';
          }
      },
      validateRetypePassword(value){
        if(value.length >= 8){
            if (value != this.newPassword) {
              this.msg = 'Password is not matching' ;
            } else {
              this.msg = '';
            }
          }
      },
    }
  
  }
  </script>
  
  <style scoped>
  .profile-page {
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 20px;
    color:#f2f2f2;
  }
  .profile-info {
    display: flex;
    align-items: center;
    margin-bottom: 20px;
  }
.profile-picture-container {
  width: 150px;
  height: 150px;
  margin-right: 20px;
  border-radius: 50%;
  overflow: hidden; /* This hides the overflowing parts of the image */
  position: relative; /* Allows positioning the image within the container */
}
.profile-picture-container img {
  width: 100%; /* Ensures the image fills the container */
  height: 100%; /* Ensures the image fills the container */
  object-fit: cover; /* Scales the image to cover the container while maintaining aspect ratio */
  position: absolute; /* Positions the image within the container (centered) */
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%); /* Centers the image within the container */
}
  .update-profile-pic{
    width: 6rem;
    border:none;
    border-radius:5px;
    margin-top:10px;
    background:#f2f2f2;
  }
  .profile-actions {
    display: flex;
    flex-direction: column;
    width: 100%;
  }
  .profile-actions h3 {
    margin-bottom: 10px;
  }
  .change-password form{
    display:flex;
    flex-direction: column;
    row-gap: 1rem;
    align-items: baseline;
  }
  </style>
  