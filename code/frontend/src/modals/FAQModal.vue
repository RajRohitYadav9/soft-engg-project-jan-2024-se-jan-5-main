<template>
    <div v-if="show" class="modal">
      <div class="modal-content">
        <header class="modal-header">
          <div v-if="title">{{ title }}</div>
        </header>
        <div class="modal-body">
            <p>{{ faq.description }}</p>
            <ul v-if="faq.attachments.length > 0">
              <li v-for="attachment in faq.attachments" :key="attachment.name">
                {{ attachment.name }}
              </li>
            </ul>
        </div>
        <footer class="modal-footer">
          <button >Close</button>
        </footer>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    props: {
      show: Boolean,
      faq: Object,
      title: String,
    },
  };
  </script>
  
  <style scoped>
  .modal {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100vh;
    background-color: rgba(0, 0, 0, 0.5);
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 100;
  }
  
  .modal-content {
    background-color: #fff;
    padding: 1rem;
    border-radius: 5px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    max-width: 800px;
    width: 100%;
  }
  
  .modal-header {
    padding: 1rem;
    border-bottom: 1px solid #ddd;
  }
  
  .modal-body {
    padding: 1rem;
  }
  
  .modal-footer {
    padding: 1rem;
    display: flex;
    justify-content: flex-end;
  }
  
  .modal-footer button {
    background-color: #007bff;
    color: #fff;
    padding: 0.5rem 1rem;
    border: none;
    border-radius: 5px;
    cursor: pointer;
  }
  </style>
  