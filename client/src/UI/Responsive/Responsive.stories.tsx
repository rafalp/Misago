import React from "react"
import { RootContainer } from "../Storybook"
import Responsive from "."

export default {
  title: "UI/Responsive",
}

export const Default = () => (
  <RootContainer padding>
    <Responsive>Default</Responsive>
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
