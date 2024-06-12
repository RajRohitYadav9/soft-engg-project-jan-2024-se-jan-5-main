import FlashMessage from './FlashMessage.vue';

export default {
  install(app) {
    const messageService = {
      successMessage(messageText, timeout) {
        const vm = app._instance; // Access Vue instance
        // console.log(vm.refs);
        try{
          vm.refs.flashMessage.addMessage(messageText, "success", timeout);
        }catch{
          return
        }
      },
      failureMessage(messageText, timeout) {
        const vm = app._instance; // Access Vue instance
        // console.log(vm.refs);
        try{
          vm.refs.flashMessage.addMessage(messageText, "failure", timeout);
        // eslint-disable-next-line no-empty
        }catch{
            return;
        }
      },

    };
    app.config.globalProperties.$flashMessage = messageService; // Register globally
    app.component('FlashMessage', FlashMessage);
  },
};
