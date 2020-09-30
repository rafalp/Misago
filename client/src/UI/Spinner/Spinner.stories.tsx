import React from "react"
import { CardContainer, RootContainer } from "../Storybook"
import Spinner from "."

export default {
  title: "UI/Spinner",
}

export const Default = () => {
  return (
    <>
      <RootContainer>
        <Spinner />
      </RootContainer>
      <CardContainer>
        <Spinner />
      </CardContainer>
    </>
  )
}

export const Small = () => {
  return (
    <>
      <RootContainer>
        <Spinner small />
      </RootContainer>
      <CardContainer>
        <Spinner small />
      </CardContainer>
    </>
  )
}
