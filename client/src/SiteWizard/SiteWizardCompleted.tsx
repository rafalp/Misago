import { Trans } from "@lingui/macro"
import React from "react"
import { ButtonPrimary } from "../UI/Button"
import { CardFooter, CardMessage } from "../UI/Card"
import { FormFooter } from "../UI/Form"
import SiteWizardContainer from "./SiteWizardContainer"

interface SiteWizardCompletedProps {
  complete: () => void
}

const SiteWizardCompleted: React.FC<SiteWizardCompletedProps> = ({
  complete,
}) => (
  <SiteWizardContainer>
    <CardMessage>
      <p className="lead">
        <Trans id="wizard.completed.lead">Basic setup completed!</Trans>
      </p>
      <p>
        <Trans id="wizard.completed.message_1">
          Your admin account has been created and you have been signed in.
        </Trans>
      </p>
      <p>
        <Trans id="wizard.start.message_2">
          Click "continue" or refresh the page to begin using your site.
        </Trans>
      </p>
    </CardMessage>
    <CardFooter>
      <FormFooter>
        <ButtonPrimary
          text={<Trans id="wizard.continue">Continue</Trans>}
          small
          onClick={complete}
        />
      </FormFooter>
    </CardFooter>
  </SiteWizardContainer>
)

export default SiteWizardCompleted
