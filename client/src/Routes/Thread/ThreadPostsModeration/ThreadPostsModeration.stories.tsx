import { withKnobs, boolean } from "@storybook/addon-knobs"
import React from "react"
import ThreadPostsModeration from "./ThreadPostsModeration"

export default {
  title: "Route/Thread/Moderation/Post Options",
  decorators: [withKnobs],
}

export const PostsOptions = () => (
  <ThreadPostsModeration
    moderation={{
      loading: boolean("Loading", false),
      actions: [
        {
          name: "Delete posts",
          icon: "fas fa-times",
          action: () => {},
        },
      ],
    }}
    selection={{ selected: [1], clear: () => {} }}
  />
)
