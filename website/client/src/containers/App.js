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
      year: 2009,
      show_results: false
    };

    this.handleChange = this.handleChange.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
    this.handlePlayerChange = this.handlePlayerChange.bind(this);
    this.handleYearChange = this.handleYearChange.bind(this);
    this.submitPlayers = this.submitPlayers.bind(this);

  }

  handleChange(event) {
    this.setState({teamname: event.target.value}, () => {
      console.log("state: " + this.state);
    });
  }

  handleSubmit(event) {
    axios.get("https://sport-site-server.herokuapp.com/depthchart/", {
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
    this.setState({[name]: value});
  }

  handleYearChange(event) {
    this.setState({year: event.target.value});
  }

  submitPlayers(event) {
    console.log(this.state);
    axios.get("https://sport-site-server.herokuapp.com/playercomp/", {
      params: {
        player1: this.state.player1,
        player2: this.state.player2,
        year: this.state.year
      }
    })
    .then( (response) => {
      console.log("response: \n");
      console.log(response.data.length);
      if (!response.data.includes(null)) {
        console.error("found null in response!")
        this.setState({stats: response.data, show_results: true});
      }
      else this.setState({stats: null, show_results: false});
      console.log(this.state);
    })
    .catch( (error) => {
      console.log(error);
      this.setState({stats: null, show_results: false});
    });
  }

  

  render() {
    return (
      <div className="App">
        {/* <DepthChart handleChange={this.handleChange} handleSubmit={this.handleSubmit} teamNames={this.getTeamNames}/> */}
        {/*<Results team={this.state}/>*/}

        <PlayerComparison handlePlayerChange={this.handlePlayerChange} handleYearChange={this.handleYearChange} submitPlayers={this.submitPlayers}/>
        <PlayerComparisonResults info={this.state} player1={this.state.player1} player2={this.state.player2}/>

      </div>
    );
  }
}

export default App;
