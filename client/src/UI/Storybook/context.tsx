import React from "react"
import { SettingsContext } from "../../Context"
import { settingsFactory } from "./factories"

export const SettingsContextFactory: React.FC = ({ children }) => (
  <SettingsContext.Provider value={settingsFactory()}>
    {children}
  </SettingsContext.Provider>
)
