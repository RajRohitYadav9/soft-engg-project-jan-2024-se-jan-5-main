<template>
  <!-- <div class="addmodal" type="button" @click=toggleModal() > -->
      <!-- <span class="addmodal" type="button" @click="toggleAddModal">+</span> -->
      <!-- + -->
  <!-- </div> -->

  <div type="create" class="full-rounded floating-button" @click=toggleModal()>
    <span>Tags</span>
    <div class="border full-rounded"></div>
  </div>
  <div class="modal" v-show="showModal">
    <div class="modal-content">
      <span class="close-button" @click=toggleModal()>&times;</span>
      <h1 class="modal-heading">Manage Tags</h1>

      <h4>Already Created Tags</h4>
      <div class="chips">
        <div v-for="tag in alreadyCreated" :key="tag" class="chip">
          <span>{{ tag.toUpperCase() }}</span>
          <button type="button" class="chip-remove" @click="deleteTag(tag)">
            x
          </button>
        </div>
    </div>
    <h4>Added Tags</h4>
      <div class="chips">
        <div v-for="tag in newTags" :key="tag" class="chip">
          <span>{{ tag.toUpperCase() }}</span>
          <button type="button" class="chip-remove" @click="removeNewTag(tag)">
            x
          </button>
        </div>
    </div>
    <div class="search-bar">
      <input
        type="text"
        v-model="searchTerm"
        placeholder="Search tags"
      />
    </div>
    <div class="error-msg">
      {{ tagErrorMessage }}
    </div>
      <div class="form" >
        <div class="button-div">
          <button  @click="addTag()" name="Add new tags">Add</button>
          <button :disabled="tagErrorMessage.length > 0" type="submit" name="create all added Tags" @click="createTags">Submit</button>
        </div>
      </div>
    </div>
  </div>
</template>
<script>


import { TICKET_TAGS_API } from "../assets/common";


export default{
  name: "FloatingTagCreateButton",
  data(){
      return {
          showModal : false,
          searchTerm: "",
          form:   {
            tags: []
          },
          allTags: [],
          newTags: [],
          alreadyCreated: [],
          tagErrorMessage:"",
      }
  },
  watch:{
    searchTerm(value){
      if(value != ""){
        this.tagErrorMessage = ""
      }
    }
  },
  mounted(){
    this.getAllTags()
  },
  methods:{
      addTag() {
        if(this.searchTerm != "" && !this.newTags.includes(this.searchTerm.toUpperCase())){
          this.form.tags.push(this.searchTerm);
          this.newTags.push(this.searchTerm)
          this.searchTerm = '';
        }
      },
      removeNewTag(tag) {
          const index = this.form.tags.indexOf(tag);
          if (index > -1) {
            this.form.tags.splice(index, 1);
          }
          const index2 = this.newTags.indexOf(tag);
          if (index2 > -1) {
            this.newTags.splice(index2, 1);
          }

      },
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

      handlePrivacyChange(){
        this.form.privacy = this.form.privacy == "public" ? "private" : "public";
      },

      async getAllTags(){
        await fetch(TICKET_TAGS_API, {
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
            this.allTags = data.message;
            this.alreadyCreated = [...data.message];
          }
          if (data.category == "error") {
            this.$flashMessage.failureMessage(data.message);
          }
        })
        .catch(() => {
          this.$flashMessage.failureMessage("Internal Server Error");
        });
      },
      async deleteTag(tag){
        await fetch(TICKET_TAGS_API, {
            method: "DELETE",
            headers: {
            "Content-Type": "application/json",
            "Web-Token" : this.$store.getters.get_web_token,
            "User-Id" : this.$store.getters.get_user_id,
            },
            body: JSON.stringify({"tag" : tag})
          })
          .then((response) => response.json())
        .then((data) => {
          if (data.category == "success") {
            const index = this.allTags.indexOf(tag);
            if (index > -1) {
              this.allTags.splice(index, 1);
            }
            const index2 = this.alreadyCreated.indexOf(tag);
            if (index2 > -1) {
              this.alreadyCreated.splice(index2, 1);
            }
          }
          if (data.category == "error") {
            this.$flashMessage.failureMessage(data.message);
          }
        })
        .catch(() => {
          this.$flashMessage.failureMessage("Internal Server Error");
        });
      },
      async createTags(){

        if(this.form.tags.length==0){
          this.tagErrorMessage = "Add atleast one tag to submit"
        }else{
            await fetch(TICKET_TAGS_API, {
                method: "POST",
                headers: {
                "Content-Type": "application/json",
                "Web-Token" : this.$store.getters.get_web_token,
                "User-Id" : this.$store.getters.get_user_id,
                },
                body: JSON.stringify(this.form)
              })
              .then((response) => response.json())
            .then((data) => {
              if (data.category == "success") {
                this.$flashMessage.successMessage(data.message);
                this.form.tags=[];
              }
              if (data.category == "error") {
                this.$flashMessage.failureMessage(data.message);
              }
            })
            .catch(() => {
              this.$flashMessage.failureMessage("Internal Server Error");
            });
          }

          this.getAllTags()
      },

  },
}

</script>

<style scoped>
.addmodal {
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
   
.addmodal:hover {
    height:88px;
    width:88px;
    font-size:68px;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 2), 0 0px 2px -1px rgba(0, 0, 0, 1);
  }
@media screen and (max-width: 440px), screen and (max-height: 600px){

  .addmodal {
     height: 48px;
     width: 48px;
     box-shadow: 0px 5px 25px 2px rgba(0,0,0,1);
     font-size: 2rem;
  }

  .addmodal:hover {
    height:46px;
    width:46px;
    font-size:58px;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 2), 0 0px 2px -1px rgba(0, 0, 0, 1);
  }
}

@media only screen and (min-width: 768px) { /* For screens wider than 768px */
      .modal-content {
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

.modal {
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

.modal-content {
  background: var(--modal-color);
  border: 1px solid var(--modal-border-color);
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
  z-index: 10000;
}

.modal-heading {
  text-align: center;
  font-size: large;
  font-weight: 200;
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

.form {
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
  column-gap:1rem;
}

.button-div button {
  background: var(--dark-button-color);
  color: #f2f2f2;
  padding: 10px 20px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: var(--medium-text-size);
  transition: 0.3s ease-in-out background-color; /* Add hover effect */
}

button[type="submit"]:hover {
  background-color: var(--dark-button-hover-color); /* Change background color on hover */
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


.search-bar {
  margin-bottom: 10px;
}
.search-bar input{
  background: var(--maindark);
  border: none;
  width: 100%;
  height: 1.5rem;
  /* padding-left: 2rem; */
  text-align: center;
  color: #f2f2f2;
  border: 1px solid #f2f2f2;
}
.search-bar input::placeholder{
color: #f2f2f2;
font-weight:100;
letter-spacing: 2px;
}
.search-bar input:focus::placeholder{
color: transparent;
}

.available-tags {
  list-style: none;
  padding: 0;
  margin: 0;
}

.available-tag {
  cursor: pointer;
  padding: 5px 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
  margin-bottom: 5px;
}

.chips {
  display: flex;
  flex-wrap: wrap;
  margin-top: 10px;
}

.chip {
  display: flex;
  align-items: center;
  padding: 5px 10px;
  margin-right: 5px;
  margin-bottom: 5px;
  border: 2px dashed #fff;
  border-radius: 4px;
  background: var(--maindark)
}

.chip span {
  margin-right: 8px;
}

.chip-remove {
  border: none;
  background-color: transparent;
  cursor: pointer;
  padding: 0;
  color: #f2f2f2;
  font-size:small;
}

.chip-remove svg {
  width: 16px;
  height: 16px;
}

.search-bar {
position: relative;
}

.suggestions {
position: absolute;
top: 100%; /* Position below the search bar */
left: 0;
background: var(--maindark);
border: 1px dashed #f2f2f2;
padding: 0;
margin: 0;
max-height: 200px; /* Limit suggestions list height */
overflow-y: auto;
z-index: 1; /* Ensure suggestions appear above other elements */
list-style: none; /* Removed list-style */
box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1); /* Optional subtle shadow */
}

.suggestion-item {
padding: 5px 10px;
cursor: pointer;
border-bottom: 1px solid black; /* Removed border-bottom */
text-align:center;
}
.suggestion-item:hover {
  background-color: rgb(5, 5, 5);
}

.error-msg{
  color: red;
}


</style>