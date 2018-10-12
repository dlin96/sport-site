import React from 'react';
import './PlayerComparison.css';
// import axios from 'axios';
// import Autosuggest from 'react-autosuggest';

function playercomparison(props) {

    return (
        <div>
            <h1>Player Comparison</h1>
            <input placeholder="Search for a player" className="search" name="player1" onChange={props.handlePlayerChange}></input>
            <br/>
            <input placeholder="and another one to compare" className="search" name="player2" onChange={props.handlePlayerChange}></input>
            <br/>
            <div className="submit">
              <button onClick={props.submitPlayers}>Submit</button>
            </div>
        </div>
    );
}

export default playercomparison