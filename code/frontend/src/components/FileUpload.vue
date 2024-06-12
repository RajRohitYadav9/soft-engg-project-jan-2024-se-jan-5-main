<template>
  <div class="upload_container">
    <div>
      <label>{{ attach_label }}</label>
      <input type="file" @change="handleFileUpload($event)" multiple />
      <br />
      <p style="font-size: 12px; margin:0;">Only <code>.jpg, .png, .gif</code> formats are allowed</p>
    </div>
  </div>
</template>

<script>
// import * as common from "../assets/common.js";

export default {
  components: {},
  emits: ["file_uploading"],
  data() {
    return {
      attachments: [],
      attach_label: this.$route.path === "/user-profile" ? "Upload photo" : "Upload files",
      user_id: this.$store.getters.get_user_id,
    };
  },
  mounted() {},
  methods: {
    fileToBase64(file) {
      return new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.readAsDataURL(file);
        reader.onload = () => resolve(reader.result);
        reader.onerror = (error) => reject(error);
      });
    },
    checkFileExtension() {},
    handleFileUpload: async function (event) {
      const files = event.target.files;
      this.attachments = [];
      for (let i = 0; i < files.length; i++) {
        try {
          const result = await this.fileToBase64(files[i]);
          let attach = {
            user_id: this.user_id,
            attachment_loc: result,
          };
          this.attachments.push(attach);
          this.$emit("file_uploading", this.attachments);
        } catch (error) {
          console.error(error);
        }
      }
    },
  },
  computed: {},
};
</script>

<style scoped>
.upload-container{
  margin-top: 5px;
}
input[type="file"]{
    width: 100%;
    padding: 12px 20px;
    margin: 8px 0;
    display: inline-block;
    border: 1px solid #ccc;
    border-radius: 4px;
    box-sizing: border-box;
}

</style>
