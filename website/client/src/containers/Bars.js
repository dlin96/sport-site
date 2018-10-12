import React, { Component } from 'react'
import { scaleLinear } from 'd3-scale'
import { interpolateLab } from 'd3-interpolate'
// import { stat } from 'fs';

export default class Bars extends Component {
  constructor(props) {
    super(props)

    this.colorScale = scaleLinear()
      .domain([0, this.props.maxValue])
      .range(["brown", "steelblue"])
      .interpolate(interpolateLab)
  }

  render() {
    const { scales, margins, data, svgDimensions, statName } = this.props
    const { xScale, yScale } = scales
    const { height } = svgDimensions

    console.log("stats: " + typeof(data[0][statName]) + " " + data[0][statName]);

    const bars = (
      data.map(datum =>
        <rect
          key={datum["player_name"]}
          x={xScale(datum["player_name"])}
          y={yScale(datum[statName])}
          height={height - margins.bottom - scales.yScale(datum[statName])}
          width={xScale.bandwidth()}
          fill={this.colorScale(datum[statName])}
        />,
      )
    )

    return (
      <g>{bars}</g>
    )
  }
}
