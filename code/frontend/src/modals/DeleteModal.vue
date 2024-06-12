<template>
    <div class="delete-modal-container">
        <div class="card">
            <p class="cookieHeading">Confirm Delete ?</p>
            <p class="cookieDescription">You can't recover your deleted ticket <br><a href="#">Are you sure?</a>.</p>

            <div class="buttonContainer">
                <button class="acceptButton" @click="$emit('delete')" >Yes</button>
                <button class="declineButton" @click="$emit('close')">Cancel </button>
            </div>

        </div>
    </div>

</template>

<script>
    export default {
        emits: ["delete", "close"],
        
    }
</script>

<style scoped>
.delete-modal-container{
    position: fixed;
    display: flex;
    justify-content: center;
    align-items: center;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    z-index: 10000;
    backdrop-filter: blur(10px);
    width: 100vw;
    height: 100vh;
}
.card {
  width: 300px;
  height: 220px;
  background-color: rgb(255, 255, 255);
  border-radius: 8px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 20px 30px;
  gap: 13px;
  position: relative;
  overflow: hidden;
  box-shadow: 2px 2px 20px rgba(0, 0, 0, 0.062);
}

#cookieSvg {
  width: 50px;
}

#cookieSvg g path {
  fill: rgb(97, 81, 81);
}

.cookieHeading {
  font-size: 1.2em;
  font-weight: 800;
  color: rgb(26, 26, 26);
}

.cookieDescription {
  text-align: center;
  font-size: 1em;
  font-weight: 400;
  color: rgb(0, 0, 0);
}

.cookieDescription a {
  --tw-text-opacity: 1;
  color: rgb(59 130 246);
}

.cookieDescription a:hover {
  -webkit-text-decoration-line: underline;
  text-decoration-line: underline;
}

.buttonContainer {
  display: flex;
  gap: 20px;
  flex-direction: row;
}

.acceptButton {
  width: 80px;
  height: 30px;
  background-color: #7b57ff;
  transition-duration: .2s;
  border: none;
  color: rgb(241, 241, 241);
  cursor: pointer;
  font-weight: 600;
  border-radius: 20px;
  box-shadow: 0 4px 6px -1px #977ef3, 0 2px 4px -1px #977ef3;
  transition: all .6s ease;
}

.declineButton {
  width: 80px;
  height: 30px;
  background-color: #dadada;
  transition-duration: .2s;
  color: rgb(46, 46, 46);
  border: none;
  cursor: not-allowed;
  font-weight: 600;
  border-radius: 20px;
  box-shadow: 0 4px 6px -1px #bebdbd, 0 2px 4px -1px #bebdbd;
  transition: all .6s ease;
}

.declineButton:hover {
  background-color: #ebebeb;
  box-shadow: 0 10px 15px -3px #bebdbd, 0 4px 6px -2px #bebdbd;
  transition-duration: .2s;
}

.acceptButton:hover {
  background-color: #9173ff;
  box-shadow: 0 10px 15px -3px #977ef3, 0 4px 6px -2px #977ef3;
  transition-duration: .2s;
}
</style>