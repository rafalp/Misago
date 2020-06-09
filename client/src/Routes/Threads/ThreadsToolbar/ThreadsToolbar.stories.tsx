import { withKnobs, boolean } from "@storybook/addon-knobs"
import React from "react"
import { RootContainer, categories } from "../../../UI/Storybook"
import ThreadsToolbar from "./ThreadsToolbar"

export default {
  title: "Route/Threads/Toolbar",
  decorators: [withKnobs],
}

export const Default = () => (
  <RootContainer padding>
    <ThreadsToolbar />
  </RootContainer>
)

export const Moderation = () => (
  <RootContainer padding>
    <ThreadsToolbar
      moderation={{
        actions: [
          {
            name: "Open",
            icon: "unlock",
            iconSolid: true,
            action: () => {},
          },
          {
            name: "Close",
            icon: "lock",
            iconSolid: true,
            action: () => {},
          },
          {
            name: "Move",
            icon: "arrow-right",
            iconSolid: true,
            action: () => {},
          },
          {
            name: "Delete",
            icon: "times",
            iconSolid: true,
            action: () => {},
          },
        ],
        disabled: boolean("Moderation disabled", false),
        loading: boolean("Moderation loading", false),
        closeThreads: () => {},
        openThreads: () => {},
        moveThreads: () => {},
        deleteThreads: () => {},
      }}
      selection={{
        clear: () => {},
      }}
    />
  </RootContainer>
)

export const Category = () => (
  <RootContainer padding>
    <ThreadsToolbar category={categories[0]} />
  </RootContainer>
)
