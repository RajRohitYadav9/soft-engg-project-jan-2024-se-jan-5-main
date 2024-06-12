<template>
    <div class="edit-modal">
      <div class="edit-modal-content">
        <span class="close-button" @click="$emit('close')">&times;</span>
        <h1 class="edit-modal-heading">Edit FAQ</h1>
        <form @submit.prevent="onSubmit">
          <label for="title">Question</label>
          <input type="title" id="title" name="title" v-model="form.question" placeholder="Enter Question" required />
          <label for="description">Description</label>
          <!-- <textarea type="description" id="description" name="description" v-model="form.description" placeholder="Enter Description" required ></textarea> -->
          <v-md-editor id="description" name="description" placeholder="Enter Description" v-model="form.solution" left-toolbar="undo redo clear | h bold italic | link code | save"  @fullscreen-change="fullscreen" ></v-md-editor>
          <FileUpload @file_uploading="onFileUpload"></FileUpload>
          <div class="button-div">
            <button type="submit">Edit</button>
          </div>
        </form>
      </div>
    </div>
</template>

<script>

import FileUpload from "../components/FileUpload.vue";
import { FAQ_API } from "../assets/common";

    export default {
        name: "FAQEditModal",
        props: ["faq"],
        components: {FileUpload},
        emits: ["faqEdited"],
        data(){
            return {
                form:  {
                    question: this.faq.question,
                    solution: this.faq.solution,
                    attachments: [],
                    tags: this.faq.tags,
                    created_by: this.$store.getters.get_username,
                }
            }
        },
        methods:{

            toggleModal(){
                this.showModal = !this.showModal
            },
            onFileUpload(value) {
            this.form.attachments.splice(0, this.form.attachments.length, ...value);
            // for (let i = 0; i < this.form.attachments.length; i++) {}
            },
            handleTags(value){
            this.form.tags = value;
            },

            onSubmit(){
            fetch(FAQ_API+`/${this.faq.faq_id}`, {
            method: "PUT",
            headers: {
                "Content-Type": "application/json",
                "Web-Token": this.$store.getters.get_web_token,
                "User-Id": this.$store.getters.get_user_id,
            },
                body: JSON.stringify(this.form),
            })
            .then((response) => response.json())
            .then((data) => {
                if (data.category == "success") {
                    this.$emit("faqEdited")
                    this.$flashMessage.successMessage(data.message);
                    
                }
                if (data.category == "error") {
                    this.$flashMessage.failureMessage(data.message);
                }
            })
            .catch(() => {
                this.$flashMessage.failureMessage("Internal Server Error");
            });
            },
            fullscreen(event){
              if(event){
                document.querySelector('.edit-modal-content').style.transform = "none";
              }else{
                document.querySelector('.edit-modal-content').style.transform = "translate(-50%,-50%)";
              }
            }
        },
        computed :{
        }
    }
</script>

<style scoped>

.addedit-modal {
    position :fixed;
    margin:0;
    /* // height:60px; */
    /* // width:60px; */
    height:90px;
    width:90px;
    border-radius: 50%;
    font-size: 70px;
    font-weight:600;
    color: white;
    bottom: 2vh;
    right: 2vw;
    /* // background-color: var(--background-color); */
    background-color: var(--login-button-hover-color);
    box-shadow: 0px 10px 35px 2px rgba(0,0,0,1);
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 100;

    cursor: pointer;

 }
     
 .addedit-modal:hover {
      height:88px;
      width:88px;
      font-size:68px;
      box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 2), 0 0px 2px -1px rgba(0, 0, 0, 1);
    }
 @media screen and (max-width: 440px), screen and (max-height: 600px){

    .addedit-modal {
       height: 48px;
       width: 48px;
       box-shadow: 0px 5px 25px 2px rgba(0,0,0,1);
       font-size: 2rem;
    }

    .addedit-modal:hover {
      height:46px;
      width:46px;
      font-size:58px;
      box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 2), 0 0px 2px -1px rgba(0, 0, 0, 1);
    }
}

@media only screen and (min-width: 768px) { /* For screens wider than 768px */
        .edit-modal-content {
            margin: 0 auto;
            background-color: white;
            padding: 20px;
            min-width: 350px; /* Set a minimum width */
            max-width: 35%; /* Set a maximum width */
            border-radius: 10px; /* Add rounded corners */
            box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.2); /* Add subtle shadow */
            transition: 0.3s ease-in-out all; /* Add smooth transition */
    }
  }
  
  .edit-modal {
/* Hidden by default */
    position: fixed; /* Stay in place */
    z-index: 100000; /* Sit on top */
    left: 0;
    top: 0;
    width: 100%; /* Full width */
    height: 100%; /* Full height */
    overflow: auto; /* Enable scroll if needed */
    background-color: rgba(0, 0, 0, 0.4); /* Black w/ opacity */
    transition: 0.3s ease-in-out all; /* Add smooth transition */
  }
  
  .edit-modal-content {
    background-color: white;
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

  .edit-modal-heading {
    text-align: center;
    font-size: large;
  }
  
  .close-button {
    color: #aaaaaa;
    float: right;
    font-size: 28px;
    font-weight: bold;
  }
  
  .close-button:hover,
  .close-button:focus {
    color: black;
    text-decoration: none;
    cursor: pointer;
  }
  
  h1 {
    text-align: center;
  }
  
  form {
    display: flex;
    flex-direction: column;
    /* align-items: center; */
  }
  
  label {
    margin-bottom: 5px;
  }
  
  input[type="title"],
  textarea[type="description"] {
    width: 100%;
    padding: 12px 20px;
    margin: 8px 0;
    display: inline-block;
    border: 1px solid #ccc;
    border-radius: 4px;
    box-sizing: border-box;
  }

  .button-div{
    display: flex;
    align-items: center;
    justify-content: center;
  }
  
  button[type="submit"] {
    background-color: var(--login-button-color);
    color: white;
    padding: 10px 20px;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    font-size: var(--medium-text-size);
    transition: 0.3s ease-in-out background-color; /* Add hover effect */
  }
  
  button[type="submit"]:hover {
    background-color: var(--login-button-hover-color); /* Change background color on hover */
  }

  .edit-modal-bottom{
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
  a{
    text-decoration: none;
    color: var(--login-button-color);
  }


.floating-button {
 font-size: 16px;
 position: fixed;
 bottom: 4vh;
 right: 4vw;
 width: 9rem;
 height: 3rem;
 margin: 0;
 padding: 1em 2.5em 1em 2.5em;
 padding:0;
 border: none;
 background: #fff;
 transition: all 0.1s linear;
 display:flex;
 justify-content: center;
 align-items: center;

}

.floating-button:active {
 transform: scale(0.95);
}

.floating-button span {
 color: #464646;
 font-weight: 600;
 letter-spacing: 2px;
}

.floating-button .border {
 position: absolute;
 border: 0.15rem solid #fff;
 transition: all 0.3s 0.08s linear;
 top: 50%;
 left: 50%;
 width: 9rem;
 height: 3rem;
 transform: translate(-50%, -50%);
 /* box-shadow: 0 0.4em 1em rgba(0, 0, 0, 0.1); */
 box-shadow: 0px 10px 35px 2px rgba(0,0,0,1);
}

.floating-button:hover .border {
 display: block;
 width: 9.9rem;
 height: 3.7rem;
}
.full-rounded {
 border-radius: 2rem;
}
</style>


