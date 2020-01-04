import React from "react"
import { CardContainer, RootContainer } from "../Storybook"
import Spinner from "."

export default {
  title: "UI/Spinner",
}

export const Default = () => {
  return (
    <>
      <RootContainer padding>
        <Spinner />
      </RootContainer>
      <CardContainer padding>
        <Spinner />
      </CardContainer>
    </>
  )
}

export const Small = () => {
  return (
    <>
      <RootContainer padding>
        <Spinner small />
      </RootContainer>
      <CardContainer padding>
        <Spinner small />
      </CardContainer>
    </>
  )
}
