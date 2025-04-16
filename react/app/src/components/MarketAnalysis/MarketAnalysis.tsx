import { Select, Slider } from "@mantine/core";
import { useState } from "react";
import PlotFromJson from "../PlotFromJson/PlotFromJson";
import classes from './MarketAnalysis.module.css' 

export function MarketAnalysis() {
    const features = [
        { value: 'launch_price_usa', label: 'Price (USA)' },
        { value: 'launch_price_pakistan', label: 'Price (Pakistan)' },
        { value: 'launch_price_india', label: 'Price (India)' },
        { value: 'launch_price_china', label: 'Price (China)' },
      ];
    

    const [feature, setFeature] = useState('launch_price_usa');
    const treemap_url = `http://localhost:8000/api/treemap/${feature}`;
    const stacked_bar_price_url = `http://localhost:8000/api/stacked_bar_price/${feature}`;
    const pie_chart_url = `http://localhost:8000/api/pie_company_counts`;

    return <div className={"MainContainer"}>
        <div className={"TitleContainer"}>
            Pricing
        </div>
        <div className={"BodyContainer"}>
            <div className={classes.GraphContainer} id={"TreeMapContainer"}>
                <div className={classes.FilterContainer}>
                    <Select
                        value={feature}
                        onChange={(val) => val && setFeature(val)}
                        data={features}
                        style={{width: "60%"}}
                        />
                </div>
                <PlotFromJson url={treemap_url}/>
            </div>
            <div className={classes.GraphContainer}>
                <PlotFromJson url={stacked_bar_price_url}/>
            </div>
            <div className={classes.GraphContainer}>
                <PlotFromJson url={pie_chart_url}/>
            </div>
            
        </div>
    </div>;
}