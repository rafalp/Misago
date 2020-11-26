import { i18n } from "@lingui/core"
import { I18nProvider } from "@lingui/react"
import { configure, addDecorator } from "@storybook/react"
import { en } from 'make-plural/plurals'
import React from "react"
import { MemoryRouter } from "react-router-dom"
import requireContext from "require-context.macro"
import messages from "../src/locale/en/messages"
import "../src/styles/index.scss"

i18n.loadLocaleData(en, { plurals: en })
i18n.load("end", messages)
i18n.activate("en")

// add memory router and I18n provider
addDecorator((storyFn) => <MemoryRouter>{storyFn()}</MemoryRouter>)
addDecorator((storyFn) => (
  <I18nProvider i18n={i18n}>
    {storyFn()}
  </I18nProvider>
))

// automatically import all files ending in *.stories.js
configure(requireContext("../src/", true, /\.stories\.tsx$/), module)

if (!document.getElementById("portals-root")) {
  const portalsRoot = document.createElement("div")
  portalsRoot.setAttribute("id", "portals-root")
  document.body.append(portalsRoot)
}
