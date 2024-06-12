<template>
  <div class="discourse-button-container" @mouseenter="showTooltip = true" @mouseleave="showTooltip = false">
    <button :class="`btn ${btnType} btn-floating`" @click="clickHandler">
      <img :src="discourseLogo" alt="Discourse" />
      <span v-if="showTooltip" class="tooltip">{{ tooltipText }}</span>
      <slot></slot>

    </button>
  </div>
</template>

<script>
import DiscourseLogo from '@/assets/discourse.svg';

export default {
  name: 'DiscourseButton',
  data() {
    return {
      discourseLogo: DiscourseLogo,
      showTooltip: false, // Controls the visibility of the tooltip
    };
  },
  props: {
    btnType: {
      type: String,
      default: 'btn-primary',
    },
    tooltipText: {
      type: String,
      default: 'Go to Discourse', // Placeholder text, adjust as needed
    },
  },
  methods: {
    clickHandler() {
      window.open('http://localhost:4200', '_blank');
    },
  },
}
</script>

<style scoped>
.discourse-button-container {
  position: fixed; /* Positioning relative to the viewport */
  bottom: 15vh; /* Distance from the bottom */
  right: 4vw; /* Distance from the right */
  cursor: pointer;
  z-index: 100;
}

.btn-floating {
  width: 60px; /* Define button width */
  height: 60px; /* Define button height */
  border-radius: 50%; /* Circular shape */
  background-color: #f2f2f2; /* Example background color */
  display: flex;
  justify-content: center;
  align-items: center;
  border: none; /* Remove default border */
  transition: background-color 0.3s, transform 0.3s;
}

.btn-floating img {
  width: 50%; /* Adjust as necessary */
  height: auto;
}

.btn-floating:hover {
  border: 2px solid #f2f2f2;
  background-color: #0056b3; /* Darker shade on hover */
  transform: scale(0.97); /* Slight decrease */
}

.tooltip {
  position: absolute;
  bottom: 100%; /* Positioned above the button */
  left: 50%; /* Center align */
  transform: translateX(-50%);
  margin-bottom: 10px;
  padding: 5px 10px;
  color: white;
  background-color: black;
  border-radius: 4px;
  font-size: 14px;
  z-index: 1;
  white-space: nowrap; /* Prevents the tooltip from wrapping */
  opacity: 0;
  visibility: hidden;
  transition: opacity 0.3s, visibility 0.3s;
}

.discourse-button-container:hover .tooltip {
  opacity: 1;
  visibility: visible;
}
</style>
