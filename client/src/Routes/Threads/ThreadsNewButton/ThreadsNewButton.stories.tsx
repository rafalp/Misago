import React from "react"
import { RootContainer, categories } from "../../../UI/Storybook"
import ThreadsNewButton from "./ThreadsNewButton"

export default {
  title: "Route/Threads/New Thread Button",
}

export const Default = () => (
  <RootContainer padding>
    <ThreadsNewButton />
  </RootContainer>
)

export const Category = () => (
  <RootContainer padding>
    <ThreadsNewButton category={categories[0]} />
  </RootContainer>
)
