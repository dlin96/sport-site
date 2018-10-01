import React from "react";

function playercompresults(props) {
    if (props.toShow === true) {
        return(
            <div>
                <h1>Results:</h1>
            </div>
        )
    } else return null;
}

export default playercompresults;