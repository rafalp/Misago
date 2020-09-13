import React from "react"
import { SettingsContextFactory } from "../../UI/Storybook"
import PostThreadAuthRequiredError from "./PostThreadAuthRequiredError"
import PostThreadPermissionDeniedError from "./PostThreadPermissionDeniedError"

export default {
  title: "Route/Post Thread",
}

export const AuthRequiredError = () => (
  <SettingsContextFactory>
    <PostThreadAuthRequiredError />
  </SettingsContextFactory>
)

export const PermissionDeniedError = () => (
  <SettingsContextFactory>
    <PostThreadPermissionDeniedError />
  </SettingsContextFactory>
)
