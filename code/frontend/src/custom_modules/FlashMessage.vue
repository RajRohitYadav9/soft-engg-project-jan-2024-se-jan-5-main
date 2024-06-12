<template>
  <div v-if="messages.length" class="flash-message">
    <ul>
      <li v-for="message in messages" :key="message.id" :class="{ 'success': message.type === 'success', 'failure': message.type === 'failure' , 'fading-out': message.fading }" @click="close(message.id)" >{{ message.text }}</li>
    </ul>
  </div>
</template>

<script>
export default {
  name: 'FlashMessage',
  data() {
    return {
      messages: [],
    };
  },
  methods: {
    addMessage(messageText, type = 'info', timeout = 1000) {
      const id = Math.random().toString(36).substring(2, 15);
      this.messages.push({ id, text: messageText, type: type , fading: false});
      setTimeout(() => {
        this.close(id);
      }, timeout);
    },
    close(id){
      const index = this.messages.findIndex(msg => msg.id === id);
      if (index > -1) {
        this.messages[index].fading = true;
        setTimeout(() => {
          this.messages.splice(index, 1);
        }, 300);
      }
      return 0;
    }
  },
};
</script>

<style scoped>
.flash-message {
  position: fixed;
  color: white;
  bottom: 10px;
  left: 10px;
  padding: 10px;
  border-radius: 4px;
  z-index: 9999; /* Ensure the message stays on top of other content */
}

.flash-message .success {
  background-color: #468847;
  color: white;
}

.flash-message .failure {
  background-color: #a94442;
  color: white;
}

.flash-message li {
  cursor: pointer;
  margin-bottom: 5px;
  padding: 1rem;
  border-radius: var(--average-border-radius);
}
.flash-message li.fading-out {
  animation: slide-left-out 0.3s ease-in-out forwards;
  opacity: 0;
}

@keyframes slide-left {
  from {
    transform: translateX(0);
  }
  to {
    transform: translateX(-100%);
  }
}

@keyframes slide-left-out {
  from {
    transform: translateX(0);
    opacity: 1;
  }
  to {
    transform: translateX(-100%);
    opacity: 0;
  }
}

</style>
