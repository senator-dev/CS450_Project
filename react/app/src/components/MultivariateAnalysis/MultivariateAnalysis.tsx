import { Select } from "@mantine/core";
import { useState } from "react";
import PlotFromJson from "../PlotFromJson/PlotFromJson";
import classes from './MultivariateAnalysis.module.css' 
import { features } from "../Interfaces";

export function MultivariateAnalysis() {
    
    const [xValue, setXValue] = useState('battery');
    const [yValue, setYValue] = useState('ram');
    const [zValue, setZValue] = useState('weight');
    const scatterUrl = `${import.meta.env.VITE_API_URL}/api/scatter_3d/${xValue}/${yValue}/${zValue}`;
    const correlationHeatmapUrl = `http://54.86.127.160:8000/api/correlation_heatmap`;

    return <div className={"MainContainer"}>
        <div className={"TitleContainer"}>
            Multivariate Analysis
        </div>
        <div className={"BodyContainer"}>
            <div className={classes.GraphContainer}>
                <div className={classes.FilterContainer}>
                    <Select
                        label="X"
                        value={xValue}
                        onChange={(val) => val && setXValue(val)}
                        data={features}
                        className={classes.Select}
                        />
                    <Select
                        label="Y"
                        value={yValue}
                        onChange={(val) => val && setYValue(val)}
                        data={features}
                        className={classes.Select}
                        />
                    <Select
                        label="Z"
                        value={zValue}
                        onChange={(val) => val && setZValue(val)}
                        data={features}
                        className={classes.Select}
                        />
                </div>
                <div className={classes.SubContainer}>
                    <PlotFromJson url={scatterUrl}/>
                </div>
            </div>
            <div className={classes.GraphContainer}>  
                <PlotFromJson url={correlationHeatmapUrl}/>
            </div>
        </div>
    </div>;
}