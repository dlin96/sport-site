import React from 'react';
import './DepthChartResults.css';

function results (props) {
    if (props.team.show_results === false) {
        return( <p> Hidden </p>)
    } else {
        var ret = [];
        var ignorekeys = ["teamname", "show_results", "team_name", "_id"];
        for (var key in props.team.dc) {
            if (ignorekeys.includes(key)) continue;
            ret.push(<li key={key} className="position">{key}: </li>);
            for (var item in props.team.dc[key]) {
                ret.push(<li key={key+"_"+item}>{props.team.dc[key][item]}</li>);
            }
        }
        return(
            <ul id="result">{ret}</ul>
        );
    }
}

export default results;