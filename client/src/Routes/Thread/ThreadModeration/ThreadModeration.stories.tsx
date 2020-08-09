import { withKnobs, boolean } from "@storybook/addon-knobs"
import React from "react"
import { RootContainer } from "../../../UI/Storybook"
import ThreadModeration from "./ThreadModeration"

export default {
  title: "Route/Thread/Moderation",
  decorators: [withKnobs],
}

export const ThreadOptions = () => (
  <RootContainer padding>
    <ThreadModeration
      moderation={{
        loading: boolean("Loading", false),
        closeThread: () => {},
        openThread: () => {},
        moveThread: () => {},
        deleteThread: () => {},
        actions: [
          {
            name: "Delete thread",
            icon: "times",
            iconSolid: true,
            action: () => {},
          },
        ],
      }}
    />
  </RootContainer>
)
