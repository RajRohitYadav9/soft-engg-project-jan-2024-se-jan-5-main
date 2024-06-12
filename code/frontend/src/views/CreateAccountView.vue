<template>
    <div class="studentHomepage13">
      <div class="supportTicketSystem">
        <div class="onlineSupportTicket">
          Online Support Ticket System
        </div>
      </div>
      <form class="rectangleParent">
        <div class="frameChild" />
        <div class="createAnAccount">Create An Account</div>
        <InputFieldContainer />
        <div class="createBtn">
          <div class="parentFrame">
            <FrameNesting
              create="Create"
              :onCreateTextClick="onCreateTextClick"
            /><FrameNesting
              create="Cancel"
              :onCreateTextClick="onCancelTextClick"
            />
          </div>
        </div>
      </form>
    </div>
  </template>
  <script>
    import { defineComponent } from "vue";
    import InputFieldContainer from "../components/InputFieldContainer.vue";
    import FrameNesting from "../components/FrameNesting.vue";
  
    export default defineComponent({
      name: "StudentHomePage",
      components: { InputFieldContainer, FrameNesting },
      methods: {
        onCreateTextClick() {
          // Please sync "Student - HomePage 12" to the project
        },
        onCancelTextClick() {
          // Please sync "Student - HomePage 12" to the project
        },
      },
    });
  </script>
<style>
    .onlineSupportTicket {
      height: 8.938rem;
      width: 47.875rem;
      position: relative;
      font-weight: 500;
      display: flex;
      align-items: center;
      justify-content: center;
      flex-shrink: 0;
      max-width: 100%;
    }
    .supportTicketSystem {
      width: 51.063rem;
      display: flex;
      flex-direction: row;
      align-items: flex-start;
      justify-content: flex-start;
      max-width: 100%;
    }
    .frameChild {
      width: 94.188rem;
      height: 63rem;
      position: relative;
      border-radius: 65px;
      background-color: #fffcfc;
      box-shadow: 20px 25px 4px rgba(0, 0, 0, 0.25),
        0px 4px 4px rgba(0, 0, 0, 0.25);
      border: 3px solid #000;
      box-sizing: border-box;
      display: none;
      max-width: 100%;
    }
    .createAnAccount {
      width: 31.688rem;
      height: 5.813rem;
      position: relative;
      font-size: 2.5rem;
      font-family: "Roboto Mono";
      color: #000;
      text-align: center;
      display: flex;
      align-items: center;
      justify-content: center;
      flex-shrink: 0;
      max-width: 100%;
      z-index: 1;
    }
    .parentFrame {
      width: 41.813rem;
      display: flex;
      flex-direction: row;
      align-items: flex-start;
      justify-content: space-between;
      gap: 1.25rem;
      max-width: 100%;
    }
    .createBtn {
      width: 44.75rem;
      display: flex;
      flex-direction: row;
      align-items: flex-start;
      justify-content: flex-end;
      max-width: 100%;
    }
    .rectangleParent {
      margin: 0;
      width: 94.188rem;
      border-radius: 65px;
      background-color: #fffcfc;
      box-shadow: 20px 25px 4px rgba(0, 0, 0, 0.25),
        0px 4px 4px rgba(0, 0, 0, 0.25);
      border: 3px solid #000;
      box-sizing: border-box;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: flex-start;
      padding: 2.813rem 1.313rem 6.75rem 1.25rem;
      gap: 2.563rem;
      max-width: 100%;
    }
    .studentHomepage13 {
      width: 100%;
      position: relative;
      background-color: #fff;
      overflow: hidden;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: flex-start;
      padding: 2.375rem 1.25rem 14.625rem 3.438rem;
      box-sizing: border-box;
      gap: 8.313rem 0rem;
      letter-spacing: normal;
      text-align: center;
      font-size: 2.5rem;
      color: #000;
      font-family: "Roboto Mono";
    }
  
    @media screen and (max-width: 1200px) {
      .studentHomepage13 {
        gap: 8.313rem 0rem;
        padding-left: 1.688rem;
        box-sizing: border-box;
      }
    }
    @media screen and (max-width: 1050px) {
      .onlineSupportTicket {
        font-size: 2rem;
      }
  
      .createAnAccount {
        font-size: 2rem;
      }
  
      .rectangleParent {
        padding-top: 1.813rem;
        padding-bottom: 4.375rem;
        box-sizing: border-box;
      }
    }
    @media screen and (max-width: 750px) {
      .parentFrame {
        flex-wrap: wrap;
      }
  
      .rectangleParent {
        gap: 2.563rem;
        padding-top: 1.25rem;
        padding-bottom: 2.813rem;
        box-sizing: border-box;
      }
  
      .studentHomepage13 {
        gap: 8.313rem 0rem;
      }
    }
    @media screen and (max-width: 450px) {
      .onlineSupportTicket {
        font-size: 1.5rem;
      }
  
      .createAnAccount {
        font-size: 1.5rem;
      }
    }
    </style>