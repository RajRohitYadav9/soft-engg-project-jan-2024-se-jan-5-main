<template>
<div class="container">
    <div class="wrapper">
        <a href="javascript:void(0);" class="like-button" :class="{'is-active' : isActive}" @click="voteTicket">
          <i class="material-icons not-liked bouncy">favorite_border</i>
          <i class="material-icons is-liked bouncy">favorite</i>
          <span class="like-overlay"></span>
        </a>
    </div>
  </div>
</template>

<script>

import {TICKET_API} from "../assets/common"

export default{
    name: "LikeButton",
    props: ["ticket_id"],
    emits: ["voted"],
    data(){
        return{
            isActive: false,
        }
    },
    mounted(){
      this.check_vote_status();
    },
    methods: {
        toggle(){
            this.isActive = !this.isActive
        },
        voteTicket(){
        if (!this.isActive){
          fetch(TICKET_API+"/vote",
            {
              method: "POST",
              headers: {
                "Content-Type": "application/json",
                "Web-Token" : this.$store.getters.get_web_token,
                "User-Id" : this.$store.getters.get_user_id,
                },
              body: JSON.stringify({
                "ticket_id" : this.ticket_id,
              })
            }
          )
          .then((response) => response.json())
          .then((data) => {
              if (data.category == "success") {
                  this.toggle()
                  this.$flashMessage.successMessage("Successfully Voted this Ticket");
              }
            }
          )
          .catch(() => {
                this.$flashMessage.failureMessage("Try Again Later");
            });
        }

        },
        check_vote_status(){
          fetch(TICKET_API+"/vote/"+this.ticket_id,
            {
              method: "GET",
              headers: {
                "Content-Type": "application/json",
                "Web-Token" : this.$store.getters.get_web_token,
                "User-Id" : this.$store.getters.get_user_id,
                },
            }
          )
          .then((response) => response.json())
          .then((data) => {
              if (data.category == "success" ) {
                  if(data.message == "voted"){
                    this.toggle()
                  }
              }
            }
          )
          .catch(() => {
            });
        }
    },
}

</script>

<style scoped>
/* 
.container {
  width: 100%;
  height: auto;
  margin: 0 auto;
  text-align: center;
  padding-top: 10%;
} */
.container .love {
  font-size: 0.9rem;
  color: #ff4f8f;
}
/* .container .wrapper {
  padding-top: 50px;
} */
.container .wrapper .like-button {
  position: relative;
  width: 35px;
  height: 35px;
  border-radius: 50%;
  background: #f2f2f2;
  display: flex;
  justify-content: center;
  align-items: center;
  margin: 0 auto;
  text-decoration: none;
  overflow: hidden;
}
.container .wrapper .like-button .like-overlay {
  display: block;
  position: absolute;
  top: 0;
  left: 0;
  width: 35px;
  height: 35px;
  border-radius: 50%;
  background: #ff4f8f;
  transform: scale(0);
  transition: all 0.4s;
  z-index: 0;
}
.container .wrapper .like-button i.not-liked {
  display: block;
  color: #000;
  position: relative;
  z-index: 1;
}
.container .wrapper .like-button i.is-liked {
  display: none;
  color: #fff;
  position: relative;
  z-index: 1;
}
.container .wrapper .like-button.is-active .like-overlay {
  transform: scale(1);
}
.container .wrapper .like-button.is-active i.not-liked {
  display: none;
}
.container .wrapper .like-button.is-active i.is-liked {
  display: block;
}

@-webkit-keyframes bouncy {
  from, to {
    -webkit-transform: scale(1, 1);
  }
  25% {
    -webkit-transform: scale(0.9, 1.1);
  }
  50% {
    -webkit-transform: scale(1.1, 0.9);
  }
  75% {
    -webkit-transform: scale(0.95, 1.05);
  }
}
@keyframes bouncy {
  from, to {
    transform: scale(1, 1);
  }
  25% {
    transform: scale(0.9, 1.1);
  }
  50% {
    transform: scale(1.1, 0.9);
  }
  75% {
    transform: scale(0.95, 1.05);
  }
}
.bouncy {
  -webkit-animation: bouncy 0.6s;
  animation: bouncy 0.6s;
  -webkit-animation-duration: 0.6s;
  animation-duration: 0.6s;
  -webkit-animation-fill-mode: both;
  animation-fill-mode: both;
}

.link-button {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  background: #6dacff;
  position: absolute;
  bottom: 20px;
  right: 20px;
  display: flex;
  justify-content: center;
  align-items: center;
  transition: all 0.4s;
}
.link-button img {
  width: 32px;
  height: 32px;
  display: block;
}
.link-button:hover {
  transform: scale(1.1) rotate(180deg);
  background: #ff4f8f;
}

</style>