import React from "react"
import { RootContainer, categories } from "../../../UI/Storybook"
import ThreadsStartButton from "./ThreadsStartButton"

export default {
  title: "Route/Threads/New Thread Button",
}

export const Default = () => (
  <RootContainer padding>
    <ThreadsStartButton />
  </RootContainer>
)

export const Category = () => (
  <RootContainer padding>
    <ThreadsStartButton category={categories[0]} />
  </RootContainer>
)
