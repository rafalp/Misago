import React from "react"
import { SettingsContextFactory } from "../Storybook"
import RouteLoader from "./RouteLoader"

export default {
  title: "Route/Loader",
}

export const Loader = () => (
  <SettingsContextFactory>
    <RouteLoader />
  </SettingsContextFactory>
)
