import React from "react"
import { SiteWizardStage } from "./SiteWizard.types"
import SiteWizardCompleted from "./SiteWizardCompleted"
import SiteWizardForm from "./SiteWizardForm"
import SiteWizardStart from "./SiteWizardStart"

const SiteWizard: React.FC = () => {
  const [stage, setStage] = React.useState<SiteWizardStage>(
    SiteWizardStage.START
  )

  switch (stage) {
    case SiteWizardStage.START:
      return (
        <SiteWizardStart complete={() => setStage(SiteWizardStage.FORM)} />
      )

    case SiteWizardStage.FORM:
      return (
        <SiteWizardForm complete={() => setStage(SiteWizardStage.COMPLETED)} />
      )

    case SiteWizardStage.COMPLETED:
      return (
        <SiteWizardCompleted
          complete={() => {
            window.location.reload()
          }}
        />
      )
  }
}

export default SiteWizard
