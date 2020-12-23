import React from "react"
import { Card, CardColorBand } from "../UI/Card"
import RouteContainer from "../UI/RouteContainer"

interface SiteWizardContainerProps {
  children: React.ReactNode
}

const SiteWizardContainer: React.FC<SiteWizardContainerProps> = ({
  children,
}) => (
  <div className="site-wizard">
    <RouteContainer>
      <div className="site-wizard-logo" />
      <Card className="site-wizard-card">
        <CardColorBand color="#FF5630" />
        {children}
      </Card>
    </RouteContainer>
  </div>
)

export default SiteWizardContainer
