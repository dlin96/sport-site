import React from "react";

function depthchart(props) {
    var teams = [
        // NFC West
        "Seahawks", "49ers", "Cardinals", "Rams",
        // NFC East
        "dallascowboys", "Giants", "Eagles", "Redskins",
        // NFC North
        "Packers", "Vikings", "Lions", "Bears",
        // NFC South
        "panthers", "Buccaneers", "Saints", "Falcons",
        // AFC East
        "Bengals", "Ravens", "Steelers", "Browns"
    ]

    var ret_teams=[];
    for (var index in teams) {
        ret_teams.push(<option key={teams[index]}>{teams[index]}</option>);
    }
    return (
        <div>
            <h1>Depth Chart</h1>
            <select onChange={props.handleChange}>
                {ret_teams}
            </select>
            <br />
            <button onClick={props.handleSubmit}>Submit</button>
        </div>
    );
}

export default depthchart;