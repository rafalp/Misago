import { withKnobs, boolean } from "@storybook/addon-knobs"
import React from "react"
import { RootContainer } from "../../../UI/Storybook"
import ThreadModerationMenu from "./ThreadModerationMenu"

export default {
  title: "Route/Thread/Moderation",
  decorators: [withKnobs],
}

export const ThreadOptions = () => (
  <RootContainer>
    <ThreadModerationMenu
      moderation={{
        loading: boolean("Loading", false),
        actions: [
          {
            name: "Delete thread",
            icon: "fas fa-times",
            action: () => {},
          },
        ],
      }}
    />
  </RootContainer>
)
