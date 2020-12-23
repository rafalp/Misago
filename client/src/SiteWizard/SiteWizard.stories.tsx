import { MockedProvider } from "@apollo/react-testing"
import { action } from "@storybook/addon-actions"
import React from "react"
import { SettingsContextFactory } from "../UI/Storybook"
import SiteWizardCompleted from "./SiteWizardCompleted"
import SiteWizardForm from "./SiteWizardForm"
import SiteWizardStart from "./SiteWizardStart"

export default {
  title: "Site Wizard",
}

export const Start = () => (
  <SiteWizardStart complete={action("complete start")} />
)

export const Form = () => (
  <MockedProvider>
    <SettingsContextFactory>
      <SiteWizardForm complete={action("complete form")} />
    </SettingsContextFactory>
  </MockedProvider>
)

export const Completed = () => (
  <SiteWizardCompleted complete={action("complete wizard")} />
)
