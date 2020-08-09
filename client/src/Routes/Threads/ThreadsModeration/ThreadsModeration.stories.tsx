import { withKnobs, boolean } from "@storybook/addon-knobs"
import React from "react"
import ThreadsModeration from "./ThreadsModeration"

export default {
  title: "Route/Threads/Moderation",
  decorators: [withKnobs],
}

export const Options = () => (
  <ThreadsModeration
    moderation={{
      disabled: boolean("Moderation disabled", false),
      loading: boolean("Moderation loading", false),
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
    }}
    selection={{
      selected: [1, 2, 3],
      clear: () => {},
    }}
  />
)
