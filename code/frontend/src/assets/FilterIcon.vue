<template>
    <!-- <div class="filter">
        <img src="@/assets/filter-10.svg" alt="filter icon" class="filter-icon" />
    </div> -->

    <button class="setting-btn" aria-label="Filter Button" >
        <span class="bar bar1"></span>
        <span class="bar bar2"></span>
        <span class="bar bar1"></span>
    </button>
</template>

<script>
export default {
    name: "FilterIcon",
    data(){
        return {
            showModal: false,
        }
    },
    methods:{
        toggleFilterModal(){
            this.showModal = !this.showMod
        }
    }
}

</script>

<style scoped>

.filter-icon{
    position: absolute;
    right: 2vw;
    margin-top: 2vh;
    height: 3rem;
    width: 3rem;
    background-color: #fff;
    padding: 0px;
    border-radius: 50%;
}
.filter-icon:hover{
    background-color: #d3d3d3;
}

/* testing */


.setting-btn {
  width: 45px;
  height: 45px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 6px;
  background-color: black;
  border-radius: 10px;
  cursor: pointer;
  border: none;
  box-shadow: 0px 0px 0px 2px rgb(177 177 177);
  position: fixed;
  right: 2vw;
  margin-top: 2vh;
  height: 3rem;
  width: 3rem;
  padding: 0px;
  border-radius: 50%;
}
.bar {
  width: 50%;
  height: 2px;
  background-color: rgb(229, 229, 229);
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  border-radius: 2px;
}
.bar::before {
  content: "";
  width: 2px;
  height: 2px;
  background-color: rgb(126, 117, 255);
  position: absolute;
  border-radius: 50%;
  border: 2px solid white;
  transition: all 0.3s;
  box-shadow: 0px 0px 5px white;
}
.bar1::before {
  transform: translateX(-4px);
}
.bar2::before {
  transform: translateX(4px);
}
.setting-btn:hover .bar1::before {
  transform: translateX(4px);
}
.setting-btn:hover .bar2::before {
  transform: translateX(-4px);
}

</style>
