import React from "react"
import { CardContainer, RootContainer } from "../Storybook"
import Icon from "."

export default {
  title: "UI/Icon",
}

const iconName = "comment-alt"

export const Regular = () => {
  const icon = <Icon icon={iconName} />

  return (
    <>
      <RootContainer padding>{icon}</RootContainer>
      <CardContainer padding>{icon}</CardContainer>
    </>
  )
}

export const Solid = () => {
  const icon = <Icon icon={iconName} solid />

  return (
    <>
      <RootContainer padding>{icon}</RootContainer>
      <CardContainer padding>{icon}</CardContainer>
    </>
  )
}

export const FixedWidth = () => {
  const icon = <Icon icon={iconName} fixedWidth />

  return (
    <>
      <RootContainer padding>{icon}</RootContainer>
      <CardContainer padding>{icon}</CardContainer>
    </>
  )
}
