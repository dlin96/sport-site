import React from 'react';

function playercomparison(props) {

    return (
        <div>
            <h1>Player Comparison</h1>
            <input name="player1" onChange={props.handlePlayerChange}></input>
            <br/>
            <input name="player2" onChange={props.handlePlayerChange}></input>
            <br/>
            <button onClick={props.submitPlayers}>Submit</button>
        </div>
    );
}

export default playercomparison