import { I18nProvider } from "@lingui/react"
import { configure, addDecorator } from "@storybook/react"
import React from "react"
import { MemoryRouter } from "react-router-dom"
import requireContext from "require-context.macro"

import "../src/styles/index.scss"

// add memory router and I18n provider
addDecorator(storyFn => <MemoryRouter>{storyFn()}</MemoryRouter>)
addDecorator(storyFn => <I18nProvider language="en">{storyFn()}</I18nProvider>)

// automatically import all files ending in *.stories.js
configure(requireContext("../src/", true, /\.stories\.tsx$/), module)

if (!document.getElementById("portals-root")) {
  const portalsRoot = document.createElement("div")
  portalsRoot.setAttribute("id", "portals-root")
  document.body.append(portalsRoot)
}
