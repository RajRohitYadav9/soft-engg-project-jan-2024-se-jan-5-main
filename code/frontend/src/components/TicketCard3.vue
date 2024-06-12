<template>
    <div class="card-content">

        <div class="center" v-for="ticket in tickets" :key="ticket.ticket_id" >
            <div @click="go(ticket.ticket_id)"  class="card">
                <div class="main-content">
                    <div class="header">
                    <span>Created on </span>
                    <span>{{ formatDate(ticket.created_on) }}</span>
                    </div>
                    <div class="double-val-label">
                      <span v-if="ticket.status=='resolved'" class="success">Resolved</span>
                      <span v-if="ticket.status=='pending'" class="primary">Open</span>
                      <!-- <span class="success">Success</span> -->
                      <span>{{ titleCase(ticket.priority) }}</span>
                    </div>
                    <p class="heading">
                        {{ ticket.title }}
                    </p>
                    <p class="description">
                        {{ markdown_to_txt(ticket.description) }}
                    </p>
                    <div class="tags">
                        <span v-for="tag in ticket.tags" :key="tag">{{tag}}</span>
                    </div>
                </div>
                <div class="more"> 
                    {{ ticket.votes }}
                </div>
                <div class="footer">By @{{ ticket.created_by }}</div>
              </div>
        </div>


    </div>
</template>

<script>
import markdownToTxt from 'markdown-to-txt';
export default {
  name: "TicketCard3",
  props: [
    "tickets",
  ],
  components: {},
  methods:{
    formatDate(value){
        var date = new Date(value*1000);
        return date.toLocaleString('en-us',{month:'short', day:'numeric'});
    },
    go(ticket_id){
      let path = ""
      if(this.$store.getters.get_logged_status){
        path = `/ticket/${ticket_id}`
      }else{
        path = `/onlyview/${ticket_id}`
      }
        this.$router.push(path);
    },
    markdown_to_txt(value){
      return markdownToTxt(value)
    },
    titleCase(st) {
      return st.toLowerCase().split(" ").reduce((s, c) =>
        s + "" + (c.charAt(0).toUpperCase() + c.slice(1) + " "), '');
    }
  }

}
</script>

<style scoped>
.card-content{
    padding:6vw;
}

.center{
    margin:2vw;
}

p.description{
    font-size: 16px;
    width: 90%;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    text-align: start;
    color: #717171;
}


.card {
  padding: 20px;
  color: white;
  background: linear-gradient(#212121, #212121) padding-box, linear-gradient(145deg, transparent 35%, #ffffff, #515759) border-box;
  border: 2px solid transparent;
  border-radius: 8px;
  display: flex;
  flex-direction: column;
  cursor: pointer;
  transform-origin: top bottom;
  transition: all 0.8s cubic-bezier(0.23, 1, 0.32, 1);
}

.card .main-content {
  flex: 1;
}

.card .header span:first-child {
  font-weight: 400;
  color: #717171;
  margin-right: 4px;
}

.card .heading {
  /* font-size: 1.3rem; */
  /* margin: 1.5rem 0 1rem; */
  font-weight: 300;
  color: #f2f2f2;
}

.card .tags {
  display: flex;
  gap: 10px;
}

.card .tags span {
  background-color: var(--dark);
  padding: 4px 8px;
  font-weight: 200;
  text-transform: uppercase;
  font-size: 12px;
  border-radius: 50em;
}

.card .footer {
  font-weight: 400;
    font-size: small;
    color: #717171;
    margin-top: 4px;
    text-align: start;
}
.card .more{
    display: flex;
    flex-direction: row;
    align-items: center;
    justify-content: flex-end;
    column-gap: 1rem;
}

.card:hover {
  /* rotate: -6deg; */
}

.double-val-label {
	display: table;
	font-family: 'Roboto', sans-serif;
	margin: 0.4em;
  float: right;
}
.double-val-label>span {
	background-color: #343434;
	color: #ffffff;
	display: table-cell;
	font-size: 0.9em;
	font-weight: 400;
	line-height: 1;
	padding: .3em .6em;
	text-align: center;
	vertical-align: baseline;
	white-space: nowrap;
}
.double-val-label>span :first-child {
		border-bottom-left-radius: 0.25em;
		border-top-left-radius: .25em;
	}
.double-val-label>span :nth-child(2) {
		border-bottom-right-radius: 0.25em;
		border-top-right-radius: .25em;
	}
.double-val-label>span.primary {
	background-color: #0a5596;
}
.double-val-label>span.success {
	background-color: #009d00;;
}

</style>