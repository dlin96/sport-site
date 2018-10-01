import React, { Component } from 'react';
import './App.css';
// import DepthChart from '../components/DepthChart/DepthChart';
// import DepthChartResults from '../components/DepthChartResults/DepthChartResults';
import PlayerComparison from '../components/PlayerComparison/PlayerComparison';
import PlayerComparisonResults from '../components/PlayerComparisonResults/PlayerComparisonResults';
import axios from 'axios';


class App extends Component {
  constructor(props) {
    super(props);
    // this.state = {
    //   teamname: "",
    //   show_results: false
    // }

    this.state = {
      player1: "",
      player2: "",
      show_results: false
    };

    this.handleChange = this.handleChange.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
    this.handlePlayerChange = this.handlePlayerChange.bind(this);
    this.submitPlayers = this.submitPlayers.bind(this);
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

  handlePlayerChange(event) {
    const name = event.target.name;
    const value = event.target.value;
    this.setState({[name]: value}, () => {
      console.log("state: " + this.state);
    })
  }

  submitPlayers(event) {
    console.log(this.state);
    axios.get("http://localhost:8000/playercomp/", {
      params: {
        player1: this.state.player1,
        player2: this.state.player2
      }
    })
    .then( (response) => {
      console.log("response: \n");
      console.log(response);
      this.setState({show_results: true})
    })
    .catch( (error) => {
      console.log(error);
    });
  }

  

  render() {
    return (
      <div className="App">
        {/* <DepthChart handleChange={this.handleChange} handleSubmit={this.handleSubmit} teamNames={this.getTeamNames}/> */}
        {/*<Results team={this.state}/>*/}

        <PlayerComparison handlePlayerChange={this.handlePlayerChange} submitPlayers={this.submitPlayers}/>
        <PlayerComparisonResults toShow={this.state.show_results}/>
      </div>
    );
  }
}

export default App;
