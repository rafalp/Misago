import { withKnobs, boolean } from "@storybook/addon-knobs"
import React from "react"
import AbsoluteContainer from "./AbsoluteContainer"

export default {
  title: "UI/AbsoluteContainer",
  decorators: [withKnobs],
}

export const Visible = () => (
  <AbsoluteContainer show>
    <p>Lorem ipsum dolor met.</p>
  </AbsoluteContainer>
)

export const Interactive = () => (
  <AbsoluteContainer show={boolean("Show", false)}>
    <p>Lorem ipsum dolor met.</p>
  </AbsoluteContainer>
)
