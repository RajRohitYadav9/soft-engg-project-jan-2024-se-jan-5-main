<template>
    <div class="card-content">
        <div class="center" v-for="faq in faqs" :key="faq.faq_id" >
            <div @click="go(`/faq/${faq.faq_id}`,faq)"  class="card">
                <div class="main-content">
                    <div class="header">
                    <span>FAQ </span>
                    </div>
                    <p class="heading">
                        {{ faq.question }}
                    </p>
                    <p class="description">
                        {{ markdown_to_txt(faq.solution) }}
                    </p>
                    <div class="tags">
                        <span v-for="tag in faq.tags" :key="tag">{{tag}}</span>
                    </div>
                </div>
                <div class="footer">By @{{ faq.created_by }}</div>
              </div>
        </div>


    </div>
</template>

<script>
import markdownToTxt from 'markdown-to-txt';
export default {
  name: "FAQCard",
  props: [
    "faqs",
  ],
  methods:{
    go(path,faq){
      this.$router.push(
        {
          path: path, 
          props: {
            faq:faq
          }
        }
      )
    },
    markdown_to_txt(value){
      return markdownToTxt(value)
    }
  }

}
</script>

<style scoped>
.card-content{
    padding:5vw;
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

</style>