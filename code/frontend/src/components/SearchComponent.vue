<template>
    <div class="search-component">
        <div class="style-7"><input type="text" name="search" placeholder="Search for A Ticket" class="style-8" v-model="query" />
            <button @click="search" aria-label="search button"  class="style-9"><svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" class="style-10">
                <path d="M21 21L14.9497 14.9497M14.9497 14.9497C16.2165 13.683 17 11.933 17 10C17 6.13401 13.866 3 10 3C6.13401 3 3 6.13401 3 10C3 13.866 6.13401 17 10 17C11.933 17 13.683 16.2165 14.9497 14.9497Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="style-11"></path>
            </svg></button></div>
    </div>
</template>

<script>

function debounce(func, wait = 500) {
  let timeout;
  return (...args) => {
    clearTimeout(timeout);
    timeout = setTimeout(() => func.apply(this, args), wait);
  };
}


export default {

    emits: [ "searched"],
    data(){
        return{
            query : "",
        }
    },
    watch:{
        'query'(value){
            this.query = value;
            this.search();
        }
    },
    methods:{
        search(){
            const update = debounce(()=>{
                this.$emit("searched", this.query);
            },500);
            update();
        }
    }

}
</script>

<style scoped>

.search-component{
    width: max-content;
    position: absolute;
    margin-top: 2.5vh;
    right: 8rem;
}

.style-7 {
        /* margin-bottom: -40px; */
        height: 2.5rem;
        transition-property: transform;
        transition-timing-function: cubic-bezier(0.4, 0, 0.2, 1);
        transition-duration: 0.15s;
        box-shadow: rgba(0, 0, 0, 0) 0px 0px 0px 0px, rgba(0, 0, 0, 0) 0px 0px 0px 0px, rgba(0, 0, 0, 0.1) 0px 10px 15px -3px, rgba(0, 0, 0, 0.1) 0px 4px 6px -4px;
        background-color: rgb(255, 255, 255);
        border-radius: 9999px;
        overflow: visible;
        max-width: 550px;
        width: 100% !important;
        display: flex;
        z-index: 21;
        position: relative;
        box-sizing: border-box;
        border-width: 0px;
        border-style: solid;
        border-color: rgb(229, 231, 235);
        padding: 0px;
    }

    .style-8 {
        box-shadow: rgba(0, 0, 0, 0) 0px 0px 0px 0px, rgba(0, 0, 0, 0) 0px 0px 0px 0px, rgba(0, 0, 0, 0.05) 0px 1px 2px 0px;
        color: rgb(8, 8, 8);
        font-weight: 400;
        font-size: 16px;
        line-height: 24px;
        font-family: Montserrat, ui-sans-serif, system-ui, sans-serif, 'Apple Color Emoji', 'Segoe UI Emoji', 'Segoe UI Symbol', 'Noto Color Emoji';
        padding-right: 8px;
        padding-left: 40px;
        padding-top: 16px;
        padding-bottom: 16px;
        background-color: rgb(255, 255, 255);
        border-style: none;
        border-start-start-radius: 9999px;
        border-end-start-radius: 9999px;
        width: 100% !important;
        display: block;
        margin-right: 1px;
        appearance: none;
        border-color: rgb(107, 114, 128);
        border-width: 0px;
        border-radius: 9999px 0px 0px 9999px;
        padding: 16px 8px 16px 40px;
        font-feature-settings: normal;
        font-variation-settings: normal;
        margin: 0px 1px 0px 0px;
        box-sizing: border-box;
    }

    .style-9 {
        transition-property: color, background-color, border-color, text-decoration-color, fill, stroke;
        transition-timing-function: cubic-bezier(0.4, 0, 0.2, 1);
        transition-duration: 0.15s;
        color: rgb(17, 17, 17);
        font-weight: 600;
        font-size: 16px;
        line-height: 24px;
        font-family: Montserrat, ui-sans-serif, system-ui, sans-serif, 'Apple Color Emoji', 'Segoe UI Emoji', 'Segoe UI Symbol', 'Noto Color Emoji';
        padding-top: 6px;
        padding-bottom: 6px;
        padding-left: 20px;
        padding-right: 20px;
        background-color: rgb(255, 255, 255);
        border-style: none;
        border-start-end-radius: 9999px;
        border-end-end-radius: 9999px;
        gap: 6px;
        align-items: center;
        cursor: pointer;
        display: flex;
        appearance: button;
        background-image: none;
        text-transform: none;
        font-feature-settings: normal;
        font-variation-settings: normal;
        margin: 0px;
        box-sizing: border-box;
        border-width: 0px;
        border-color: rgb(229, 231, 235);
    }

    .style-10 {
        transition-property: color, background-color, border-color, text-decoration-color, fill, stroke;
        transition-timing-function: cubic-bezier(0.4, 0, 0.2, 1);
        transition-duration: 0.15s;
        color: rgb(17, 17, 17);
        width: 1.25rem !important;
        height: 20px;
        display: block;
        vertical-align: middle;
        box-sizing: border-box;
        border-width: 0px;
        border-style: solid;
        border-color: rgb(229, 231, 235);
        padding: 0px;
        margin: 0px;
    }

    .style-11 {
        box-sizing: border-box;
        border-width: 0px;
        border-style: solid;
        border-color: rgb(229, 231, 235);
        padding: 0px;
        margin: 0px;
    }

    .style-12 {
        box-sizing: border-box;
        border-width: 0px;
        border-style: solid;
        border-color: rgb(229, 231, 235);
        padding: 0px;
        margin: 0px;
    }

</style>