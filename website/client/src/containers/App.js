import React, { Component } from 'react';
import './App.css';
import DepthChart from '../components/DepthChart/DepthChart';
import Results from '../components/Results/Results';
import axios from 'axios';


class App extends Component {
  constructor(props) {
    super(props);
    this.state = {
      teamname: "",
      show_results: false
    }

    this.handleChange = this.handleChange.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
  }

  handleChange(event) {
    this.setState({teamname: event.target.value}, () => {
      console.log("state: " + this.state);
    });
  }

  handleSubmit(event) {
    axios.get("http://localhost:8000/depthchart/", {
      params: {
        teamname: this.state.teamname
      }
    })
      .then( (response) => {
        console.log("response: \n");
        console.log(response);
        this.setState({dc: null});
        this.setState({dc: response["data"][0]}, function() {
          this.setState({show_results: true})
        })
      })
      .catch( (error) => {
        console.log(error);
      });
  }

  

  render() {
    return (
      <div className="App">
        <DepthChart handleChange={this.handleChange} handleSubmit={this.handleSubmit} teamNames={this.getTeamNames}/>
        <br />

        <Results team={this.state}/>
      </div>
    );
  }
}

export default App;
