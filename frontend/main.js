const app = new Vue({
  el: "#app",
  data: {
    tags: [],
    tagId: null,
    url: "https://www.youtube.com/watch?v=oyEuk8j8imI",
    downloadUrls: [],
    loading: false,
  },
  methods: {
    async getInfo() {
      if (!this.url) return;

      if (!this.http) {
        this.http = axios.create({});
      }

      this.loading = true;
      const { data } = await this.http.post("http://localhost:5000/getInfo", {
        url: this.url,
      });
      this.loading = false;

      this.tags = data;
    },

    async download(itag) {
      this.tagId = itag;
      this.loading = true;

      if (this.validateInput()) {
        const { data } = await this.http.post(
          `http://localhost:5000/download`,
          {
            url: this.url,
            itag,
          }
        );
        this.downloadUrls.push(data);
      }

      this.loading = false;
    },

    validateInput() {
      return this.url.trim().length > 0;
    },
  },
});
