import React, { Component } from 'react';
import '../node_modules/bootstrap/dist/css/bootstrap.min.css';
import InputGroup from './InputGroup.js';
import axios from 'axios';

import ResultTable from './d3/ResultTable.js';
import './App.css';

class App extends Component {
  state = {
    player: {},
    player2: {},
    showResults: false
  }

  handleSubmit = () => {
    axios.get('http://localhost:8000/comparison/', {
      params: {
        player: this.state.player['name'],
        player2: this.state.player2['name']
      }  
    })
          .then(response => {
            this.setState({
              player: {...this.state.player, stats: response.data[0]},
              player2: {...this.state.player2, stats: response.data[1]},
              showResults: true
            });
              console.log(this.state.player, this.state.player2);
          });          
  }

  handleOnChangeP1 = (event) => {
      this.setState({
        player: {name: event.target.value}
      })
  }

  handleOnChangeP2 = (event) => {
    this.setState({
      player2: {name: event.target.value}
    })
  }

  render() {
    let results = null;

    if(this.state.showResults) {
      results = (
        <div>
          <ResultTable player={this.state.player} player2={this.state.player2}/>
        </div>
      );
    }

    return (
      <div className="App">
        <InputGroup submit={this.handleSubmit} change={this.handleOnChangeP1} change2={this.handleOnChangeP2}/>
        {results}
      </div>
    );
  }
}

export default App;
