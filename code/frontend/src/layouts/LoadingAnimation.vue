<template>
    <div class="loader">
        <div class="dot"></div>
        <div class="dot"></div>
        <div class="dot"></div>
    </div>

</template>
<script>
</script>
<style scoped>


.loader {
  display: flex;
  align-items: center;
  justify-content: center;
  column-gap: 2rem;
  width: 100vw;
  height: 100vh;
  margin: 0 auto;
  position: absolute;
  z-index: 1000;
  background-color: var(--maindark);

}

@keyframes leap {
  0% {
    transform: translateY(0);
  }

  7% {
    transform: scale(1);
  }

  25% {
    transform: scale(1.3);
  }

  50% {
    transform: scale(1);
    opacity: 0.5;
  }

  75% {
    transform: translateY(10px);
  }

  100% {
    transform: translateY(0);
  }
}

.dot {
  width: 20px;
  height: 20px;
  border-radius: 100%;
}

.dot:nth-child(1) {
  background-color: #e26ee5;
  animation: leap 1s ease-in-out alternate 0.4s infinite;
}

.dot:nth-child(2) {
  background-color: #7e30e1;
  animation: leap 1s ease-in-out alternate 0.6s infinite;
}

.dot:nth-child(3) {
  background-color: #efe704;
  animation: leap 1s ease-in-out alternate 0.8s infinite;
}

</style>