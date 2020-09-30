import React from "react"
import { RootContainer, categories } from "../../../UI/Storybook"
import ThreadsToolbar from "./ThreadsToolbar"

export default {
  title: "Route/Threads/Toolbar",
}

export const Default = () => (
  <RootContainer>
    <ThreadsToolbar />
  </RootContainer>
)

export const Category = () => (
  <RootContainer>
    <ThreadsToolbar category={categories[0]} />
  </RootContainer>
)
