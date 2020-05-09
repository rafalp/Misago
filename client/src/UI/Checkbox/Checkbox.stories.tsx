import React from "react"
import { RootContainer } from "../Storybook"
import Checkbox from "."

export default {
  title: "UI/Checkbox",
}

export const Default = () => {
  return (
    <RootContainer padding>
      <Checkbox />
    </RootContainer>
  )
}

export const Checked = () => {
  return (
    <RootContainer padding>
      <Checkbox checked />
    </RootContainer>
  )
}

export const Disabled = () => {
  return (
    <RootContainer padding>
      <Checkbox disabled />
    </RootContainer>
  )
}

export const DisabledAndChecked = () => {
  return (
    <RootContainer padding>
      <Checkbox checked disabled />
    </RootContainer>
  )
}
