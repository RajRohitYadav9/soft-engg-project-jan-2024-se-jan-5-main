<template>
    <div class="checkbox-wrapper">
    <input @change="toggle()" id="terms-checkbox-37" name="checkbox" type="checkbox" :checked="solved" >
    <label class="terms-label" for="terms-checkbox-37">
        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 200 200" class="checkbox-svg">
        <mask fill="white" id="path-1-inside-1_476_5-37">
            <rect height="200" width="200"></rect>
        </mask>
        <rect mask="url(#path-1-inside-1_476_5-37)" stroke-width="40" class="checkbox-box" height="200" width="200"></rect>
        <path stroke-width="15" d="M52 111.018L76.9867 136L149 64" class="checkbox-tick"></path>
        </svg>
        <span class="label-text">{{text}}</span>
    </label>
    </div>
</template>
<script>

import {TICKET_API} from "../assets/common"
    export default{
        name: "SolveButton",
        props: ["solved", "ticket_id"],
        data(){
            return{
                ticket_solved: this.solved,
            }
        },
        computed:{
          text(){
            if(this.ticket_solved){
              return "Solved"
            }else{
              return "Solve"
            }
          }
        },
        methods:{
            async toggle(){
                if (!this.ticket_solved){
                      const response = await fetch(TICKET_API+"/solve", {
                        method: "POST",
                        headers: {
                            "Content-Type": "application/json",
                            "Web-Token" : this.$store.getters.get_web_token,
                            "User-Id" : this.$store.getters.get_user_id,
                        },
                        body: JSON.stringify({"ticket_id" : this.ticket_id})
                      });

                      const data = await response.json();
                      if(data.category == "success"){
                        this.$flashMessage.successMessage(data.message);
                        this.ticket_solved=true;
                      }else{
                        this.$flashMessage.failureMessage(data.message);
                      }
                      return;
                }else{
                      const response = await fetch(TICKET_API+"/unsolve", {
                        method: "POST",
                        headers: {
                            "Content-Type": "application/json",
                            "Web-Token" : this.$store.getters.get_web_token,
                            "User-Id" : this.$store.getters.get_user_id,
                        },
                        body: JSON.stringify({"ticket_id" : this.ticket_id})
                      });

                      const data = await response.json();
                      if(data.category == "success"){
                        this.$flashMessage.successMessage(data.message);
                        this.ticket_solved=false;
                      }else{
                        this.$flashMessage.failureMessage(data.message);
                      }
                      return;

                }
            }
        }
    }
</script>

<style scoped>

.checkbox-wrapper input[type="checkbox"] {
  display: none;
}

.checkbox-wrapper .terms-label {
  cursor: pointer;
  display: flex;
  align-items: center;
}

.checkbox-wrapper .terms-label .label-text {
  margin-left: 10px;
}

.checkbox-wrapper .checkbox-svg {
  width: 30px;
  height: 30px;
}

.checkbox-wrapper .checkbox-box {
  fill: #f2f2f2;
  stroke: #f2f2f2;
  stroke-dasharray: 800;
  stroke-dashoffset: 800;
  transition: stroke-dashoffset 0.6s ease-in;
}

.checkbox-wrapper .checkbox-tick {
  stroke: #f2f2f2;
  stroke-dasharray: 172;
  stroke-dashoffset: 172;
  transition: stroke-dashoffset 0.6s ease-in;
}

.checkbox-wrapper input[type="checkbox"]:checked + .terms-label .checkbox-box,
  .checkbox-wrapper input[type="checkbox"]:checked + .terms-label .checkbox-tick {
  stroke-dashoffset: 0;
}
.checkbox-wrapper input[type="checkbox"]:checked + .terms-label .checkbox-box{
    fill:transparent;
}

</style>