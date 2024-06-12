<template>
<div class="modal">

    <div class="modal-content">
        <span class="close-button" @click="$emit('close')">&times;</span>
    <h1 class="modal-heading">Filter</h1>
    <form @submit.prevent="onSubmit">
        <label  class="top-label" for="status">Status</label>
        <div class='radio-container-1'>
                <input @change="validate" id='status-resolved' name='status' type='radio' v-model="form.filter_status" value='resolved'>
                <label  for='status-resolved'>Resolved</label>
                <input @change="validate" id='status-pending' name='status' type='radio' v-model="form.filter_status" value='pending'>
                <label  for='status-pending'>Pending</label>
        </div>

        <label class="top-label" for='sort-by'>Sort By</label>
        <div class='sort_by'>
            <div class='radio-container-1'>
                <input id='sort-by-asc' name='sort-by-asc'  v-model="form.sortdir" type='radio' value='asc'>
                <label for='sort-by-asc'>Ascending</label>
                <input id='sort-by-desc' name='sort-by-asc'  v-model="form.sortdir" type='radio' value='desc'>
                <label for='sort-by-desc'>Descending</label>
            </div>
        </div>

        <label  class="top-label" for='group-by'>Group By</label>
        <div class='group_by'>
            <div class='radio-container-2'>
                <input  v-if="form.filter_status=='pending'"  id='group-by-created' name='group-by-created'  v-model="form.sortby" type='radio' value='created_on'>
                <label  v-if="form.filter_status=='pending'" for='group-by-created'>Created On</label>
                <input  v-if="form.filter_status=='resolved'" id='group-by-resolved' name='group-by-resolved'  v-model="form.sortby" type='radio' value='resolved_on'>
                <label  v-if="form.filter_status=='resolved'" for='group-by-resolved'>Resolved On</label>
                <input  id='group-by-votes' name='group-by-votes'  v-model="form.sortby" type='radio' value='votes' >
                <label for='group-by-votes'>Votes</label>
            </div>
        </div>
        <label  class="top-label" for='filter_by_priority'>Filter By</label>
        <div class='filter_by_priority'>
            <div class='radio-container-2'>
                <input   id='filter-by-high' name='filter-by-high'  v-model="form.filter_priority" type='radio' value='high'>
                <label  for='filter-by-high'>High</label>
                <input   id='filter-by-medium' name='filter-by-medium'  v-model="form.filter_priority" type='radio' value='medium'>
                <label  for='filter-by-medium'>Medium</label>
                <input  id='filter-by-low' name='filter-by-low'  v-model="form.filter_priority" type='radio' value='low' >
                <label for='filter-by-low'>Low</label>
            </div>
        </div>
        
        <div class="top-label check">
          <label for="check">Clear All</label>
            <input @click="clearFilter" type="checkbox" name="check" />
        </div>

        <label class="top-label" for='group-by'>Group By Tags</label>
        <div class='tags_by'>
            <AddTags @addTag="handleTags"></AddTags>
        </div>

        <div class="center-button">
          <a @click="filtered()">
                SAVE
            <span></span>
          </a>
        </div>
    </form>
</div>

</div>

</template>

<script>
import AddTags from "@/components/AddTags.vue"
export default {
    emits: ["close", "filtered"],
    props: {"filters": Object},
    components: {AddTags},
    data () {
        return {
          form : {}
        }
    },
    methods: {
        validate(){
            if(this.form.filter_status === "resolved" && this.form.sortby == "created_on"){
                this.form.sortby = "resolved_on";
                
              }
            if(this.form.filter_status =="pending" && this.form.sortby == "resolved_on"){
                this.form.sortby = "created_on";
                
            }
        },
        filtered(){
            // set filter state in local storage
            // filter type are 2 types -> my_ticket, all_ticket
            // save filter settings in local storage
          
            let filter_obj = Object.assign({}, this.form)
            this.$emit("filtered",filter_obj)
        },
        handleTags(value){
          this.form.filter_tags = value;
        },
        clearFilter(){
          this.form =  {
              query: "",
              filter_tags: [],
              filter_status: "",
              filter_priority: "",
              sortby: "",
              sortdir:"",
          }
        }

    },
    created(){
      this.form = Object.assign({},this.filters);
    },

}
</script>

<style scoped>

.top-label{
  margin-top:1rem;
}

@import url("https://fonts.googleapis.com/css?family=Montserrat:400,600&display=swap");

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
  }
  
  .modal {
    position: fixed; /* Stay in place */
    z-index: 100; /* Sit on top */
    left: 0;
    top: 0;
    width: 100%; /* Full width */
    height: 100%; /* Full height */
    overflow: auto; /* Enable scroll if needed */
    background-color: rgba(0, 0, 0, 0.4); /* Black w/ opacity */
    transition: 0.3s ease-in-out all; /* Add smooth transition */
  }
  
  .modal-content {
    /* background: rgba(24, 20, 20, 1); */
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
    font-weight: 200;
  }

  form {
    display: flex;
    flex-direction: column;
    /* align-items: center; */
  }
  
  .top-label {
    margin-bottom: 5px;
  }

  .center-button {
    text-align: center;
}

.center-button a {
  position: relative;
  display: inline-block;
  padding: 10px 20px;
  color: #ffffff;
  font-size: 16px;
  text-decoration: none;
  text-transform: uppercase;
  overflow: hidden;
  transition: .5s;
  margin-top: 2rem;
  letter-spacing: 3px;
  cursor: pointer;
}

.center-button a:hover {
  background: #f2f2f2;
  color: #000000;
  border-radius: 5px;
}

.center-button a span {
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

.center-button a span:nth-child(1) {
  bottom: 2px;
  left: -100%;
  width: 100%;
  height: 2px;
  background: linear-gradient(90deg, transparent, #f2f2f2);
  animation: btn-anim1 2s linear infinite;
}



.right-container .pets-photo button i {
  color: rgba(0, 0, 0, 0.8);
  font-size: 16px;
}
.right-container .pets-weight .radio-container {
  display: flex;
  justify-content: space-between;
  width: 100%;
}
.right-container footer {
  align-items: center;
  background: #fff;
  display: grid;
  padding: 5px 40px;
}
.right-container footer button {
  border: 1px solid rgba(0, 0, 0, 0.2);
  height: 38px;
  line-height: 38px;
  width: 100px;
  border-radius: 19px;
  font-family: "Montserrat", sans-serif;
}
.right-container footer #back {
  background: #fff;
  transition: 0.2s all ease-in-out;
}
.right-container footer #back:hover {
  background: #171A2B;
  color: white;
}
.right-container footer #next {
  background: #807182;
  border: 1px solid transparent;
  color: #fff;
}
.right-container footer #next:hover {
  background: #171A2B;
}

.pets-name label, .pets-breed label, .pets-birthday label, .pets-gender label, .pets-spayed-neutered label, .pets-weight label {
  display: block;
  margin-bottom: 5px;
}

.radio-container-1, .radio-container-2{
    /* background: #454545; */
    background: var(--maindark);
    border: 1px solid rgba(0, 0, 0, 0.1);
    border-radius: 4px;
    /* display: inline-block; */
    display: flex;
}

.radio-container-1 label {
  background: transparent;
  border: 1px solid transparent;
  border-radius: 2px;
  display: inline-block;
  height: 26px;
  line-height: 26px;
  margin: 0;
  padding: 0;
  text-align: center;
  transition: 0.2s all ease-in-out;
  width: 100%;
  color: white;
}
.radio-container-2 label {
  background: transparent;
  border: 1px solid transparent;
  border-radius: 2px;
  height: 26px;
  line-height: 26px;
  margin: 0;
  padding: 0;
  text-align: center;
  transition: 0.2s all ease-in-out;
  width: 100%;
  color: white;
  flex-direction: row;
  justify-content: space-between;
  overflow: hidden;
}

.radio-container-1 input[type=radio] {
  display: none;
}
.radio-container-2 input[type=radio] {
  display: none;
}

.radio-container-1 input[type=radio]:checked + label {
  /* background: #F7B1AB; */
    background: #7100ab;
    /* background: #f2f2f2; */
    border: 1px solid rgba(0, 0, 0, 0.1);
    border-radius: 5px;
    color: white;
}
.radio-container-2 input[type=radio]:checked + label {
    background: #51009b;
  /* background: #f2f2f2;; */
  border: 1px solid rgba(0, 0, 0, 0.1);
  color: #ffffff;
  border-radius: 5px;
}

.check{
  display: flex;
  flex-direction: row;
  column-gap: 2rem;
  align-items:center;
}
.check input{
  margin:0;
}

</style>