import React from "react"
import { RootContainer, categories } from "../../../UI/Storybook"
import ThreadsNewButton from "./ThreadsNewButton"

export default {
  title: "Route/Threads/New Thread Button",
}

export const Default = () => (
  <RootContainer>
    <ThreadsNewButton />
  </RootContainer>
)

export const Category = () => (
  <RootContainer>
    <ThreadsNewButton category={categories[0]} />
  </RootContainer>
)
