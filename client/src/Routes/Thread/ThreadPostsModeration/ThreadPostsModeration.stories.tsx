import { withKnobs, boolean } from "@storybook/addon-knobs"
import React from "react"
import ThreadPostsModeration from "./ThreadPostsModeration"

export default {
  title: "Route/Thread/PostsModeration",
  decorators: [withKnobs]
}

export const Menu = () => (
  <ThreadPostsModeration
    moderation={{
      loading: boolean("Loading", false),
      deletePosts: () => {},
      actions: [
        {
          name: "Delete posts",
          icon: "times",
          iconSolid: true,
          action: () => {},
        },
      ],
    }}
    selection={{ selected: [1], clear: () => {} }}
  />
)
