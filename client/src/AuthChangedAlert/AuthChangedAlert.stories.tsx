import { i18n } from "@lingui/core"
import { I18nProvider } from "@lingui/react"
import { actions } from "@storybook/addon-actions"
import { withKnobs, text } from "@storybook/addon-knobs"
import React from "react"
import AuthChangedLoggedInAlert from "./AuthChangedLoggedInAlert"
import AuthChangedLoggedOutAlert from "./AuthChangedLoggedOutAlert"

export default {
  title: "Auth/Alert",
  decorators: [withKnobs],
}

const { reload } = actions({
  reload: "reload app",
})

export const LoggedIn = () => (
  <I18nProvider i18n={i18n}>
    <AuthChangedLoggedInAlert
      username={text("User name", "JohnDoe")}
      reload={reload}
    />
  </I18nProvider>
)

export const LoggedOut = () => (
  <I18nProvider i18n={i18n}>
    <AuthChangedLoggedOutAlert
      username={text("User name", "JohnDoe")}
      reload={reload}
    />
  </I18nProvider>
)
