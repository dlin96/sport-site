/*
 * filename: depthchart.js
 * purpose: front-end logic for Ajax requests to server. 
 */ 
const url="http://localhost:8000/depth-chart/";

new Vue({
	el: '#app',
	data: {
	     selected: '',
         results: []
	},
	methods: {
        getTeam: () => {
            console.log(this.selected);
		    let config = {
				params: {
					teamname: 'panthers'
				}
			}
            console.log(config);
		    axios.get(url, config).then( function(response) {
			    this.results = response.data;
                console.log(this.results);
		    })
        }
	}
});
