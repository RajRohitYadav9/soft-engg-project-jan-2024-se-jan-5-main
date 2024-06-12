<!-- eslint-disable vue/multi-word-component-names -->
<template>
    <div class="detailed-page">
      <div class="topic-header">
        <h2>placeholder title</h2>
        <div class="topic-actions">
          <button @click="likeTopic">Like </button>
        </div>
      </div>
      <div class="topic-content">
        <p>topic_description</p>
        <div v-if="5 > 0" class="attachments">
          <h3>Attachments</h3>
          <ul>
            <li v-for="attachment in [1,2,3,4]" :key="attachment">
              <a :href="attachment" target="_blank">attachments</a>
            </li>
          </ul>
        </div>
      </div>
      <div class="reply-section">
        <h3>Replies</h3>
        <ul class="replies">
          <li v-for="reply in [1,2]" :key="reply">
            <div class="reply-author">
              (Staff)
            </div>
            <p>{{ reply }}</p>
            <button @click="likeReply(0)">Like 1</button>
          </li>
        </ul>
        <form @submit.prevent="submitReply">
          <textarea v-model="newReplyContent" placeholder="Write your reply..."></textarea>
          <button type="submit">Reply</button>
        </form>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    // props: {
    //   topic: Object,
    // },
    data() {
      return {
        newReplyContent: '',
      };
    },
    methods: {
      likeTopic() {
        // Handle liking the topic (update likes count)
        // this.topic.likes++;
      },
      likeReply(replyId) {
        // Handle liking a reply (update reply's likes count)
        const reply = this.topic.replies.find(r => r.id === replyId);
        if (reply) {
          reply.likes++;
        }
      },
    //   submitReply() {
    //     // Handle submitting a new reply (add to replies array)
    //     if (this.newReplyContent.trim()) {
    //       this.topic.replies.push({
    //         id: Date.now(), // Generate a unique ID (replace with actual ID generation)
    //         staffName: 'Your Name', // Replace with staff name
    //         content: this.newReplyContent,
    //         likes: 0,
    //       });
    //       this.newReplyContent = '';
    //     }
    //   },
    },
  };
  </script>

  <style scoped>
  .detailed-page {
    padding: 2rem;
    background-color: #f5f5f5;
    max-width: 700px; /* Set a maximum width for responsiveness */
    margin: 0 auto; /* Center the page horizontally */
  }
  
  @media (max-width: 768px) {
    /* Styles for screens less than 768px wide */
    .detailed-page {
      padding: 1rem;
    }
  }
  
  .topic-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 1rem;
    font-size: 1.2rem; /* Adjust heading size */
  }
  
  .topic-content {
    margin-bottom: 1rem;
  }
  
  .attachments {
    margin-top: 1rem;
  }
  
  .attachments li {
    margin-bottom: 0.5rem;
  }
  
  .reply-section {
    border-top: 1px solid #ddd;
    padding-top: 1rem;
  }
  
  .replies {
    list-style: none;
    padding: 0;
  }
  
  .replies li {
    margin-bottom: 1rem;
    padding: 1rem;
    border: 1px solid #ddd;
    border-radius: 4px;
    background-color: #fff;
  }
  
  .reply-author {
    font-weight: bold;
    margin-bottom: 0.5rem;
  }
  </style>