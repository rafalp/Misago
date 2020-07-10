import { withKnobs, boolean } from "@storybook/addon-knobs"
import React from "react"
import FixedContainer from "./FixedContainer"

export default {
  title: "UI/FixedContainer",
  decorators: [withKnobs],
}

export const Visible = () => (
  <FixedContainer show>
    <p>Lorem ipsum dolor met.</p>
  </FixedContainer>
)

export const Interactive = () => (
  <FixedContainer show={boolean("Show", false)}>
    <p>Lorem ipsum dolor met.</p>
  </FixedContainer>
)
