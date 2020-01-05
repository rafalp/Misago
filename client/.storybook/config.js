import { configure, addDecorator } from "@storybook/react"
import React from "react"
import { MemoryRouter } from "react-router-dom"
import requireContext from "require-context.macro"

import "../src/styles/index.scss"

// add memory router
addDecorator(storyFn => (
  <MemoryRouter>
    {storyFn()}
  </MemoryRouter>
))

// add modal root for portals
addDecorator(storyFn => (
  <>
    {storyFn()}
    <div id="modals-root" />
  </>
))

// automatically import all files ending in *.stories.js
configure(requireContext("../src/", true, /\.stories\.tsx$/), module)
