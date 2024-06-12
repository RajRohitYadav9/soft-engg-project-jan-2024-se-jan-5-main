<template>
    <div class="search-and-add-tags">

    <div class="chips">
        <div v-for="tag in selectedTags" :key="tag" class="chip">
          <span>{{ tag.toUpperCase() }}</span>
          <button type="button" class="chip-remove" @click="removeTag(tag)">
            x
          </button>
        </div>
      </div>
      <div class="search-bar">
        <input
          type="text"
          v-model="searchTerm"
          placeholder="Search tags"
          @keyup="showSuggestions"
        />
        <ul v-if="showSuggestionsList && filteredTags.length > 0" class="suggestions">
          <li
            v-for="suggestion in filteredTags.slice(0, 3)" 
            :key="suggestion"
            class="suggestion-item"
            @click="addTag(suggestion)"
          >
            {{ suggestion.toUpperCase() }}
          </li>
        </ul>
      </div>

    </div>
  </template>
  
  <script>
  import { TICKET_TAGS_API } from '../assets/common';
  import {show_error_and_logout} from "../utils"
  export default {
    data() {
      return {
        searchTerm: '',
        availableTags: [],
        selectedTags: [],
        showSuggestionsList: false,
      };
    },
    methods: {
      addTag(tag) {
        if (!this.selectedTags.includes(tag)) {
          this.selectedTags.push(tag);
          this.searchTerm = '';
          this.showSuggestionsList = false;
        }
        this.$emit("addTag", this.selectedTags);
      },
      removeTag(tag) {
        const index = this.selectedTags.indexOf(tag);
        if (index > -1) {
          this.selectedTags.splice(index, 1);
        }
      },
      showSuggestions() {
        this.showSuggestionsList = this.searchTerm.length > 0; // Show suggestions only when there's input
      },
      async getAllTags(){
        fetch(TICKET_TAGS_API, {
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
            // this.flashMessage.success({
            //   message: `Total ${data.message.length} Tickets retrieved.`,
            // });
            this.availableTags = data.message;
          }
          if (data.category == "error") {
              show_error_and_logout(this,data.message);
          }
        })
        .catch(() => {
          // this.$log.error(`Error : ${error}`);
          // this.flashMessage.error({
          //   message: "Internal Server Error",
          // });
          this.$flashMessage.failureMessage("Internal Server Error");
        });
    }
    },
    computed: {
      filteredTags() {
        if(this.searchTerm != ""){
                const lowerSearchTerm = this.searchTerm.toLowerCase();
                return this.availableTags.filter((tag) =>tag.toLowerCase().includes(lowerSearchTerm))
        }else{
            return []
        }
        },
    },
    async mounted(){
      await this.getAllTags();
    }

  };
  </script>
  
  <style scoped>
  .search-and-add-tags {
    /* display: flex;
    /* flex-direction: column; */
    /* flex-direction: row;
    justify-content: space-between;
    align-items: center; */ 
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

  </style>
  