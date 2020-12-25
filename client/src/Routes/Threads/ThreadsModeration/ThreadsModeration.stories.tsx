import { withKnobs, boolean } from "@storybook/addon-knobs"
import React from "react"
import ThreadsModerationMenu from "./ThreadsModerationMenu"

export default {
  title: "Route/Threads/Moderation",
  decorators: [withKnobs],
}

export const Options = () => (
  <ThreadsModerationMenu
    moderation={{
      disabled: boolean("Moderation disabled", false),
      loading: boolean("Moderation loading", false),
      actions: [
        {
          name: "Open",
          icon: "fas fa-unlock",
          action: () => {},
        },
        {
          name: "Close",
          icon: "fas fa-lock",
          action: () => {},
        },
        {
          name: "Move",
          icon: "fas fa-arrow-right",
          action: () => {},
        },
        {
          name: "Delete",
          icon: "fas fa-times",
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
