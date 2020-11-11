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
    <RootContainer>
      <ThreadPost
        post={{
          id: "1",
          richText: [
            {
              id: "aaaa",
              type: "p",
              text: "Lorem ipsum dolor met sit amet elit.",
            },
          ],
          edits: 0,
          postedAt: "2020-04-01T21:42:51Z",
          posterName: username,
          poster: userFactory({ name: username }),
          extra: {},
        }}
        threadId="1"
        threadSlug="test-thread"
      />
    </RootContainer>
  )
}

export const PostSelectable = () => {
  const username = text("Poster name", "John")

  return (
    <RootContainer>
      <ThreadPost
        post={{
          id: "1",
          richText: [
            {
              id: "aaaa",
              type: "p",
              text: "Lorem ipsum dolor met sit amet elit.",
            },
          ],
          edits: 0,
          postedAt: "2020-04-01T21:42:51Z",
          posterName: username,
          poster: userFactory({ name: username }),
          extra: {},
        }}
        threadId="1"
        threadSlug="test-thread"
        isSelected={false}
        toggleSelection={action("Toggle selection")}
      />
    </RootContainer>
  )
}

export const PostByDeletedUser = () => {
  const username = text("Poster name", "John")

  return (
    <RootContainer>
      <ThreadPost
        post={{
          id: "1",
          richText: [
            {
              id: "aaaa",
              type: "p",
              text: "Lorem ipsum dolor met sit amet elit.",
            },
          ],
          edits: 0,
          postedAt: "2020-04-01T21:42:51Z",
          posterName: username,
          poster: null,
          extra: {},
        }}
        threadId="1"
        threadSlug="test-thread"
      />
    </RootContainer>
  )
}

export const PostAfterAnother = () => (
  <RootContainer>
    <ThreadPost
      post={{
        id: "1",
        richText: [
          {
            id: "aaaa",
            type: "p",
            text: "Lorem ipsum dolor met sit amet elit.",
          },
        ],
        edits: 0,
        postedAt: "2020-04-01T21:42:51Z",
        posterName: "John",
        poster: null,
        extra: {},
      }}
      threadId="1"
      threadSlug="test-thread"
    />
    <ThreadPost
      post={{
        id: "2",
        richText: [
          {
            id: "bbbb",
            type: "p",
            text: "Lorem ipsum dolor met sit amet elit.",
          },
        ],
        edits: 0,
        postedAt: "2020-04-03T15:22:11Z",
        posterName: "Doe",
        poster: null,
        extra: {},
      }}
      threadId="1"
      threadSlug="test-thread"
    />
  </RootContainer>
)
