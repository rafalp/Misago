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
  <AuthChangedLoggedInAlert
    username={text("User name", "JohnDoe")}
    reload={reload}
  />
)

export const LoggedOut = () => (
  <AuthChangedLoggedOutAlert
    username={text("User name", "JohnDoe")}
    reload={reload}
  />
)
