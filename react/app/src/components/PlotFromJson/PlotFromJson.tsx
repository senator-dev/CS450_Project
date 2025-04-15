import React, { useEffect, useRef, useState } from 'react';
import Plotly from 'plotly.js-dist-min';
import axios from 'axios';


interface PlotFromJsonProps {
    url: string
}

const PlotFromJson: React.FC<PlotFromJsonProps> = ({ url }) => {
  const [plotData, setPlotData] = useState<any>(null);
  const plotRef = useRef<HTMLDivElement | null>(null);

  useEffect(() => {
    axios.get(url) 
      .then(res => {
        setPlotData(res.data);
      })
      .catch(err => console.error('Error fetching plot data:', err));
  }, [url]);


  useEffect(() => {
    if (plotRef.current && plotData) {
      Plotly.newPlot(
        plotRef.current,
        plotData.data,
        plotData.layout,
        plotData.config || {}
      );
    }
  }, [plotData]);

  return <div
    ref={plotRef}
    className="PlotlyFigure"
  />
};

export default PlotFromJson;