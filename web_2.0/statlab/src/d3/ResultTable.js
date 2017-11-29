import React from 'react';
import '../App.css';

const ResultTable = (props) => {
    return (
        <table>
            <thead>
                <tr>
                    <th>{props.player['name']}</th>
                    <th>Stats</th>
                    <th>{props.player2['name']}</th>
                </tr>
            </thead>
            <tbody>
            </tbody>
        </table>
    );
}

export default ResultTable;