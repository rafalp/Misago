import { withKnobs, boolean } from "@storybook/addon-knobs"
import React from "react"
import { RootContainer, categories } from "../../../UI/Storybook"
import ThreadsToolbar from "./ThreadsToolbar"

export default {
  title: "Route/Threads/Toolbar",
  decorators: [withKnobs],
}

export const Default = () => (
  <RootContainer>
    <ThreadsToolbar acl={{ start: boolean("acl.start", true) }} />
  </RootContainer>
)

export const Category = () => (
  <RootContainer>
    <ThreadsToolbar
      acl={{ start: boolean("acl.start", true) }}
      category={categories[0]}
    />
  </RootContainer>
)
