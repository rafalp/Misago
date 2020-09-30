import { withKnobs, boolean } from "@storybook/addon-knobs"
import React from "react"
import { RootContainer } from "../Storybook"
import Responsive from "."

export default {
  title: "UI/Responsive",
  decorators: [withKnobs],
}

export const Default = () => (
  <RootContainer>
    <Responsive>Always visible</Responsive>
    <Responsive mobile>Mobile</Responsive>
    <Responsive mobile tablet>
      Mobile + Tablet
    </Responsive>
    <Responsive mobile desktop>
      Mobile + Desktop
    </Responsive>
    <Responsive tablet>Tablet</Responsive>
    <Responsive tablet desktop>
      Tablet + Desktop
    </Responsive>
    <Responsive desktop>Desktop</Responsive>
  </RootContainer>
)

export const Configurable = () => (
  <RootContainer>
    <Responsive
      desktop={boolean("desktop", false)}
      tablet={boolean("tablet", false)}
      mobile={boolean("mobile", false)}
      landscape={boolean("landscape", false)}
      portrait={boolean("portrait", false)}
    >
      Visible!
    </Responsive>
  </RootContainer>
)
