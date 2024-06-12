<template>
    <div class="container">
        <div class="modal">
            <span class="close-button" @click="$emit('close')">&times;</span>
            <div class="modal__header">
                <div class="input">
                    <label class="input__label">Reply</label>
                    <!-- <textarea class="input__field input__field--textarea"></textarea> -->
                    <v-md-editor  v-model="form.solution" left-toolbar="undo redo | tip" ></v-md-editor>
                </div>
                <FileUpload @file_uploading="onFileUpload" style="margin-top: 1rem;"></FileUpload>
            </div>
            <div class="modal__footer">
                <button class="button button--primary" @click="reply">Reply</button>
            </div>
        </div>
    </div>
</template>

<script>

import { TICKET_REPLY } from "@/assets/common.js";

import FileUpload from "../components/FileUpload.vue"
    export default {
        name: "ReplyModal",
        props: ["ticket_id"],
        emits: ["close"],
        components: {FileUpload},
        data(){
            return{
              form: {
                  ticket_id: this.ticket_id,
                  solution: "",
                  attachments: [],
              }
            }
        },
        methods:{
          reply(){
              fetch(TICKET_REPLY,{
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
                if(data.category == "success"){
                  this.$flashMessage.successMessage("Successfully Replied");
                  this.$emit("replied")
                  return;
                }
                if (data.category == "error"){
                    this.$flashMessage.failureMessage(data.message);
                    return;
                }
            })
            .catch(() => {
                this.$flashMessage.failureMessage("Internal Server Error");
            })
            this.$emit("close");

          },
          onFileUpload(value) {
            this.form.attachments.splice(0, this.form.attachments.length, ...value);
          },
      },
    }
</script>

<style scoped>
  .close-button {
    color: #000000;
    float: right;
    font-size: 28px;
    font-weight: 200;
    position: relative;
    padding-right: 1vw;
    text-align: end;
  }
  
  .close-button:hover,
  .close-button:focus {
    font-weight:800;
    text-decoration: none;
    cursor: pointer;
  }
  
.button {
  /* appaerance: none; */
  font: inherit;
  border: none;
  background: none;
  cursor: pointer;
}

.container {
    display: flex;
    align-items: center;
    justify-content: flex-end;
    padding: 1.5rem;
    padding-left: 0;
}

.modal {
  display: flex;
  flex-direction: column;
  width: 90%;
  color: #f2f2f2;
  background-color: #252525;
  box-shadow: 0 15px 30px 0 rgba(0, 26, 35, 0.15);
  border-radius: 10px;
}

.modal__header {
  padding: 1rem 1.5rem;
  border-bottom: 1px solid #ddd;
  /* display: flex; */
  align-items: center;
  justify-content: space-between;
}

.modal__body {
  padding: 1rem 1rem;
}

.modal__footer {
  padding: 0.5rem 1.5rem 1.5rem;
  text-align: end;
}

.modal__title {
  font-weight: 700;
  font-size: 1.25rem;
}

.button {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  transition: 0.15s ease;
}

.button--icon {
  width: 2.5rem;
  height: 2.5rem;
  background-color: transparent;
  border-radius: 0.25rem;
}

.button--icon:focus, .button--icon:hover {
  background-color: #ededed;
}

.button--primary {
  background: var(--dark-button-color);
  color: #f2f2f2;
  border: 1px solid #7b7a7a;
  padding: 0.75rem 1.25rem;
  border-radius: 0.25rem;
  font-weight: 500;
  font-size: 0.875rem;
}

.button--primary:hover {
  background-color: var(--dark-button-hover-color);
}

.input {
  display: flex;
  flex-direction: column;
}

.input + .input {
  margin-top: 1.75rem;
}

.input__label {
  font-weight: 300;
    /* font-size: 0.875rem; */
    margin-bottom: 1rem;
}

.input__field {
  display: block;
  margin-top: 0.5rem;
  border: 1px solid #DDD;
  border-radius: 0.25rem;
  padding: 0.75rem 0.75rem;
  transition: 0.15s ease;
}

.input__field:focus {
  outline: none;
  border-color: #007dab;
  box-shadow: 0 0 0 1px #007dab, 0 0 0 4px rgba(0, 125, 171, 0.25);
}

.input__field--textarea {
  min-height: 100px;
  max-width: 100%;
}

.input__description {
  font-size: 0.875rem;
  margin-top: 0.5rem;
  color: #8d8d8d;
}
</style>