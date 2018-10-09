import React from "react";
import BarChart from '../../containers/BarChart';
import './PlayerComparisonResults.css';

function playercompresults(props) {

    const statsMap = {
        "passing_yds": "Passing Yds",
        "passing_cmp": "Passes Cmp",
        "passing_att": "Passing Attempts",
        "pass_pct": "Completion %",
        "passing_tds": "Passing TDs",
        "rushing_yds": "Rushing Yds",
        "rushing_tds": "Rushing TDs",
        "rushing_att": "Rushing Attempts",
        "receiving_yds": "Receiving Yds",
        "receiving_tds": "Receiving TDs",
        "receiving_tar": "Targets",
        "receiving_rec": "Receptions",
        "receiving_yac_yds": "YAC", 
        "ypc": "YPC",
    };

    if (props.info.show_results === true) {
        let stats = [];
        let player1 = props.info.stats[0];
        let player2 = props.info.stats[1];
        for (var val in props.info.stats[0]) {
            if (val !== "player_name") {
                let p1Stat = Number(player1[val]);
                let p2Stat = Number(player2[val]);
                let p1Bg, p2Bg = "white";

                if(p1Stat > p2Stat) {
                    p1Bg = "green";
                    p2Bg = "red";
                } else if (p2Stat > p1Stat) {
                    p1Bg = "red";
                    p2Bg = "green";
                }

                stats.push(
                    <tr>
                        <td style={{'background-color': p1Bg}}>{player1[val]}</td>
                        <td>{statsMap[val]}</td>
                        <td style={{'background-color': p2Bg}}>{player2[val]}</td>
                    </tr>);
            }
        }
        return(
            <div>
                <h1>Results:</h1>
                <table>
                    <tbody>
                        <tr>
                            <th>{player1["player_name"]}</th>
                            <th>Stats</th>
                            <th>{player2["player_name"]}</th>
                        </tr>
                        {stats}
                    </tbody>
                </table>
                <BarChart />
            </div>
        )
    } else return null;
}

export default playercompresults;