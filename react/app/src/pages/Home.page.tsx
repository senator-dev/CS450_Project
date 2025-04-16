import './Home.page.css'
import { MultivariateAnalysis } from '@/components/MultivariateAnalysis/MultivariateAnalysis';
import { TechnicalHistory } from '@/components/TechnicalHistory/TechnicalHIstory';
import { MarketAnalysis } from '@/components/MarketAnalysis/MarketAnalysis';



export function HomePage() {
  return (
    <div className={"HomePage"}>
      <div className={"PageContainer"}>
        <div style={{display: "flex", alignItems: "center", justifyContent: "center", fontSize: "40px", fontWeight: "bolder"}}>
          Mobiles Dataset
        </div>
        <MultivariateAnalysis />
        <TechnicalHistory />
        <MarketAnalysis />
      </div>
    </div>
  );
}

