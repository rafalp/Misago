import { Trans } from "@lingui/macro"
import React from "react"
import { ButtonPrimary } from "../UI/Button"
import { CardFooter, CardMessage } from "../UI/Card"
import { FormFooter } from "../UI/Form"
import SiteWizardContainer from "./SiteWizardContainer"

interface SiteWizardStartProps {
  complete: () => void
}

const SiteWizardStart: React.FC<SiteWizardStartProps> = ({ complete }) => (
  <SiteWizardContainer>
    <CardMessage>
      <p className="lead">
        <Trans id="wizard.start.lead">Welcome to your Misago site!</Trans>
      </p>
      <p>
        <Trans id="wizard.start.message_1">
          Before you will be able to use your site, you will have to setup an
          admin account and few basic options.
        </Trans>
      </p>
      <p>
        <Trans id="wizard.start.message_2">
          Don't worry about getting something wrong. You can change your
          choices through the admin panel at any time.
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

export default SiteWizardStart
