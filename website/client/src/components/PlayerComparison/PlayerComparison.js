import React from 'react';
import './PlayerComparison.css';
// import axios from 'axios';
// import Autosuggest from 'react-autosuggest';

function playercomparison(props) {
    let years = [];
    for(let year=2009; year < 2017; year++) {
        years.push(<option value={year}>{year}</option>);
    }

    return (
        <div>
            <h1>Player Comparison</h1>
            <input placeholder="Search for a player" className="search" name="player1" onChange={props.handlePlayerChange}></input>
            <br/>
            <input placeholder="and another one to compare" className="search" name="player2" onChange={props.handlePlayerChange}></input>
            <br/>
            <select onChange={props.handleYearChange}>
              {years}
            </select>
            <br/><br/>
            <div className="submit">
              <button onClick={props.submitPlayers}>Submit</button>
            </div>
        </div>
    );
}

export default playercomparison