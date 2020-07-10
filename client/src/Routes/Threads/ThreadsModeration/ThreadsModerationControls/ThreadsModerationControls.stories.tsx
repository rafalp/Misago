import { withKnobs, boolean } from "@storybook/addon-knobs"
import React from "react"
import ThreadsModerationControls from "./ThreadsModerationControls"

export default {
  title: "Route/Threads/Moderation/Controls",
  decorators: [withKnobs],
}

export const ModerationControls = () => (
  <ThreadsModerationControls
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
      selected: [1, 2, 3],
      clear: () => {},
    }}
  />
)
