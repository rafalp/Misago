import React from "react"
import { CardContainer, RootContainer } from "../Storybook"
import Icon from "."

export default {
  title: "UI/Icon",
}

export const Regular = () => {
  const icon = <Icon icon="far fa-comment-alt" />

  return (
    <>
      <RootContainer>{icon}</RootContainer>
      <CardContainer>{icon}</CardContainer>
    </>
  )
}

export const Solid = () => {
  const icon = <Icon icon="fas fa-comment-alt" />

  return (
    <>
      <RootContainer>{icon}</RootContainer>
      <CardContainer>{icon}</CardContainer>
    </>
  )
}

export const FixedWidth = () => {
  const icon = <Icon icon="far fa-comment-alt" fixedWidth />

  return (
    <>
      <RootContainer>{icon}</RootContainer>
      <CardContainer>{icon}</CardContainer>
    </>
  )
}
