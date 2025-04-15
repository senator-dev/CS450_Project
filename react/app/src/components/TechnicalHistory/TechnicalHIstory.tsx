import { Select, Slider } from "@mantine/core";
import { useState } from "react";
import PlotFromJson from "../PlotFromJson/PlotFromJson";
import classes from './TechnicalHistory.module.css' 
import { features } from "../Interfaces";

export function TechnicalHistory() {

    const [year, setYear] = useState(2025);
    const [feature, setFeature] = useState('battery');
    const violin_chart_url = `http://host.docker.internal:8080/api/violin_chart/${feature}/${year}`;

    return <div className={"MainContainer"}>
        <div className={"TitleContainer"}>
            Technical Specifications
        </div>
        <div className={"BodyContainer"}>
            <div className={classes.GraphContainer}>
                <PlotFromJson url={"http://host.docker.internal:8080/api/parallel_coordinates"}/>
            </div>
            <div className={classes.GraphContainer}>
                <div className={classes.FilterContainer}>
                    <Select
                        value={feature}
                        onChange={(val) => val && setFeature(val)}
                        data={features}
                        className={classes.Select}
                        />
                    <Slider
                        min={2014}
                        max={2025}
                        step={1}
                        marks={[
                            { value: 2025, label: '2025' },
                            { value: 2019, label: '2019' },
                            { value: 2014, label: '2014' }

                        ]}
                        onChange={(val) => val && setYear(val)}
                        value={year}
                        className={classes.Slider}
                        color="rgb(255, 150, 100)"
                        />
                </div>
                <div className={classes.SubContainer}>
                    <PlotFromJson url={violin_chart_url}/>
                </div>
            </div>
        </div>
    </div>;
}