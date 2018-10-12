import React, { Component } from 'react'
import './App.css'
import {scaleBand, scaleLinear} from 'd3-scale';
import Axes from './Axes';
import Bars from './Bars';

class BarChart extends Component {
   constructor(props){
      super(props);
      this.xScale = scaleBand();
      this.yScale = scaleLinear();
   }
   
render() {
    const margins = { top: 50, right: 20, bottom: 100, left: 60 }
    const svgDimensions = { width: 400, height: 500 }

    //const maxValue = 50;
    const maxValue = Math.max(...this.props.data.map(player => player[this.props.statName])) * 1.1;
    console.log(maxValue);

    // const data = [{"name": "Tom Brady", "passing_tds": 33}, {"name": "Ben Roethlisberger", "passing_tds": 23}, {"name": "average", "passing_tds":16}];
    const data = this.props.data;
    console.log(data);
    
    // scaleBand type
    const xScale = this.xScale
      .padding(0.5)
      // scaleBand domain should be an array of specific values
      // in our case, we want to use movie titles
      .domain(this.props.data.map(player => player["player_name"]))
      .range([margins.left, svgDimensions.width - margins.right])
  
     // scaleLinear type
    const yScale = this.yScale
       // scaleLinear domain required at least two values, min and max       
      .domain([0, maxValue])
      .range([svgDimensions.height - margins.bottom, margins.top])

    return (
        <svg width={svgDimensions.width} height={svgDimensions.height}>
            <Axes
            scales={{ xScale, yScale }}
            margins={margins}
            svgDimensions={svgDimensions}
            />
            <Bars
            scales={{ xScale, yScale }}
            margins={margins}
            data={this.props.data}
            maxValue={maxValue}
            svgDimensions={svgDimensions}
            statName={this.props.statName}
            />
        </svg>        
    )
   }
}
export default BarChart