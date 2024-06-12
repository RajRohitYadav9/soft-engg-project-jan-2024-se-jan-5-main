<!-- eslint-disable vue/multi-word-component-names -->
<template>
    <svg width="48" height="48" viewBox="0 0 48 48" :style="{ fill : voted ? '#871f1f':'grey' }" xmlns="http://www.w3.org/2000/svg" @click="voteClicked">
    <path d="M15 8C8.925 8 4 12.925 4 19C4 30 17 40 24 42.326C31 40 44 30 44 19C44 12.925 39.075 8 33 8C29.28 8 25.99 9.847 24 12.674C22.9857 11.2292 21.6382 10.0501 20.0715 9.23649C18.5049 8.42289 16.7653 7.99875 15 8Z" :style="{stroke : voted? '#871f1f' : 'grey'}" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>
    </svg>
    <!-- <div class="placement">
        <div @click="voteClicked" class="heart" :class="{isactive: isActive}" ></div>
    </div> -->
</template>
<script>

export default {
    data(){
        return{
            voted : false,
            isActive:false,
        }
    },
    methods: {
        voteClicked(){
            this.voted = true;
            this.isActive = !this.isActive;
        },
    },
    computed:{
    }
}
    
</script>
<style scoped>
svg{
    width:24px;
    height:24px;
}

.heart {
    width:100%;
    height:100%;
    background: url("https://cssanimation.rocks/images/posts/steps/heart.png") no-repeat;
    background-position: 0 0;
    background-size:cover;
    cursor: pointer;
    transition: background-position 0.5s steps(28);
    transition-duration: 0s;
}
.heart.isactive {
    transition-duration: 1s;
    background-position: -600px 0;
}

/* body {
  background: #000000;
} */

.placement {
    width:24px;
    height:24px;
}
    
</style>