import { action } from "@storybook/addon-actions"
import { withKnobs, text } from "@storybook/addon-knobs"
import React from "react"
import { RootContainer, userFactory } from "../../../UI/Storybook"
import ThreadPost from "./ThreadPost"

export default {
  title: "Route/Thread/Post",
  decorators: [withKnobs],
}

export const PostByUser = () => {
  const username = text("Poster name", "John")

  return (
    <RootContainer padding>
      <ThreadPost
        post={{
          id: "1",
          body: { text: "Lorem ipsum dolor met sit amet elit." },
          edits: 0,
          postedAt: "2020-04-01T21:42:51Z",
          posterName: username,
          poster: userFactory({ name: username }),
          extra: {},
        }}
      />
    </RootContainer>
  )
}

export const PostSelectable = () => {
  const username = text("Poster name", "John")

  return (
    <RootContainer padding>
      <ThreadPost
        post={{
          id: "1",
          body: { text: "Lorem ipsum dolor met sit amet elit." },
          edits: 0,
          postedAt: "2020-04-01T21:42:51Z",
          posterName: username,
          poster: userFactory({ name: username }),
          extra: {},
        }}
        isSelected={false}
        toggleSelection={action("Toggle selection")}
      />
    </RootContainer>
  )
}

export const PostByDeletedUser = () => {
  const username = text("Poster name", "John")

  return (
    <RootContainer padding>
      <ThreadPost
        post={{
          id: "1",
          body: { text: "Lorem ipsum dolor met sit amet elit." },
          edits: 0,
          postedAt: "2020-04-01T21:42:51Z",
          posterName: username,
          poster: null,
          extra: {},
        }}
      />
    </RootContainer>
  )
}

export const PostAfterAnother = () => (
  <RootContainer padding>
    <ThreadPost
      post={{
        id: "1",
        body: { text: "Lorem ipsum dolor met sit amet elit." },
        edits: 0,
        postedAt: "2020-04-01T21:42:51Z",
        posterName: "John",
        poster: null,
        extra: {},
      }}
    />
    <ThreadPost
      post={{
        id: "2",
        body: { text: "Lorem ipsum dolor met sit amet elit." },
        edits: 0,
        postedAt: "2020-04-03T15:22:11Z",
        posterName: "Doe",
        poster: null,
        extra: {},
      }}
    />
  </RootContainer>
)
