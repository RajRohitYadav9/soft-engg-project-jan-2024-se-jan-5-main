<template>
          <div class="card">
            <!-- <div class="card_product-img">
              <img class="card_img" alt="product-image" :src="img_url" />
            </div> -->
            <div class="card_content">
              <div class="card_name">{{
              title }}</div>
              <div class="card_content-bottom">
                <div class="card_history">
                  <div class="icon">
                    <!-- <img src="" alt="icon"> -->
                    <p >{{value}}</p>
                  </div>
                </div>
                <div class="card_time">
                  <div class="icon">
                  </div>
                  <share></share>
                </div>
              </div>
            </div>
  
          </div>

  </template>
  
  
  <script>

import share from "../assets/share.vue";
  export default {
      // eslint-disable-next-line vue/multi-word-component-names
      name: "Card",
      props:{ "title" : String, "value": String},
      components: {share},
      data () {
          return {
          }
      },
      computed:{
        img_url(){
            return `https://picsum.photos/200/300?text=${this.title}`;
        }
        
      }

  }
  </script>
  
  <style scoped>
  
  
  .icon {
    display: flex;
  }
  a{
    text-decoration: none;
  }
  img.card_img{
    vertical-align: middle;
    height: 100%;
    width: 100%;
  
  }
  
  .card_container{
    display: flex;
    align-items: flex-start;
    flex-wrap:wrap;
    gap: 100px;
    justify-content: space-around;
    padding-left:40px;
    padding-right:40px;
  }
  
  .card {
    display: flex;
    flex-direction: column;
  
    background-color: var(--card-background-color);
    /* color: var(--card-text-color); */
    color: rgb(156 0 217);
    border-radius: 16px;
    padding: 15px;
    margin:5px;
    width: 300px;
    /* height: 250px; */
    height: 15rem;
    max-height: 300px;
    
    box-shadow: 0 25px 50px 0 rgba(0,0,0,0.5);
    z-index: 1;
  }
    @media screen and (max-width: 680px),screen and (max-height: 600px) {
      .card{
        font-size: 0.7rem;
        width: 200px;
        padding-bottom: 10px;
      }
    }
    .card_product-img {
      border-radius: 8px;
    }
    .card_content {
      flex: 3;
      display: flex;
      flex-direction: column;
      flex-wrap: wrap;
      gap: 5px;
      padding: 5px 0 5px 0;
      bottom: 1;
      height: auto;
      overflow-wrap: break-word;
      word-break:break-word;
    }
      @media screen and (max-width: 400px), screen and (max-height: 600px) {
        .card_content {
        gap: 8px;
        padding: 5px;
        }
      }
      .card_name {
        flex:1;
        color: white;
        font-size: 1.2rem;
        margin:10px;
        cursor: pointer;
      }
        .card_name:hover {
          color: var(--main-color);
        }
      
      .card_description {
        font-size: auto;
        font-size: 0.9rem;
        font-weight: lighter;
        margin-top: auto;
        margin-bottom: auto;
    
        overflow-wrap: break-word;
      }
      .card_content-bottom {
        flex:0.5;
        padding-bottom: auto;
        display: flex;
        justify-content: space-between;
        padding-top: auto;
        height: auto;
        align-items: center;
      }
        @media screen and (max-width: 400px), screen and (max-height: 600px) {
            .card_content-bottom{
            padding-top: 2px;
            }

        }
        .card_content-bottom {
          display: flex;
          align-items: center;
          gap: 5px;
          font-weight: 400;
        }
        .card_content-bottom .card_history {
          color: var(--deeper_color);
        }
        .card_content-bottom p{
          margin-top: 0;
          margin-bottom: 2px;
          font-size: x-large;
        }

  .card-time{
    display: contents;
  }
      


  
  </style>