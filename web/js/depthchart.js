const url = "http://localhost:8000/depth-chart/";
let config= {
    headers: {
        Content-Type: 'application/javascript'
    },
	params: {
		teamname: 'panthers'
	}
};

console.log("script");
new Vue({
	el: '#app',
	data: {
		results: []
	},
	mounted() {
		axios.get(url, config).then(response => {
			this.results = response.data;
		})
	}
});
