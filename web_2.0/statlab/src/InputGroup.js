import React from 'react';

const inputGroup = (props) => {
    return (
        <div>
            <input type="text" id="player" onChange={props.change} name="typeahead" className="form-control typeahead tt-query border border-primary" autoComplete="off" spellCheck="false" placeholder="Type a player's name"/>
            <br />
            <br />
            <input type="text" id="player2" onChange={props.change2} name="typeahead" className="form-control typeahead tt-query border border-primary" autoComplete="off" spellCheck="false" placeholder="Type a player's name"/>
            <br />
            <button type="button" className="btn btn-primary btn-lg" onClick={props.submit}>Submit</button>
        </div>
    )
};

export default inputGroup;