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
  <I18nProvider language="en">
    <AuthChangedLoggedInAlert
      username={text("User name", "JohnDoe")}
      reload={reload}
    />
  </I18nProvider>
)

export const LoggedOut = () => (
  <I18nProvider language="en">
    <AuthChangedLoggedOutAlert
      username={text("User name", "JohnDoe")}
      reload={reload}
    />
  </I18nProvider>
)
