import './Home.page.css'
import { MultivariateAnalysis } from '@/components/MultivariateAnalysis/MultivariateAnalysis';
import { TechnicalHistory } from '@/components/TechnicalHistory/TechnicalHIstory';
import { MarketAnalysis } from '@/components/MarketAnalysis/MarketAnalysis';



export function HomePage() {
  return (
    <div className={"HomePage"}>
      <div className={"PageContainer"}>
        <MultivariateAnalysis />
        <TechnicalHistory />
        <MarketAnalysis />
      </div>
    </div>
  );
}

