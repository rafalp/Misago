import React from "react"
import { RootContainer } from "../UI/Storybook"
import RootLoader from "."

export default {
  title: "Pages/Root loader",
}

export const Default = () => {
  return (
    <RootContainer>
      <RootLoader />
    </RootContainer>
  )
}
