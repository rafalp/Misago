import { withKnobs, boolean } from "@storybook/addon-knobs"
import React from "react"
import { RootContainer } from "../../../UI/Storybook"
import ThreadModeration from "./ThreadModeration"

export default {
  title: "Route/Thread/Moderation",
  decorators: [withKnobs],
}

export const ThreadOptions = () => (
  <RootContainer>
    <ThreadModeration
      loading={boolean("Loading", false)}
      actions={[
        {
          name: "Delete thread",
          icon: "fas fa-times",
          action: () => {},
        },
      ]}
    />
  </RootContainer>
)
