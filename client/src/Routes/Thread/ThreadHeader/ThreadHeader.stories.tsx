import { MockedProvider } from "@apollo/react-testing"
import { withKnobs, boolean, number, text } from "@storybook/addon-knobs"
import React from "react"
import { RootContainer, categories, userFactory } from "../../../UI/Storybook"
import ThreadHeader from "./ThreadHeader"

export default {
  title: "Route/Thread/Header",
  decorators: [withKnobs],
}

export const ThreadByUser = () => (
  <RootContainer padding>
    <ThreadHeader
      acl={{ edit: false }}
      moderation={null}
      thread={{
        id: "1",
        title: text(
          "Title",
          "First observed by the astronomer Galileo Galilei!"
        ),
        slug: "test-slug",
        replies: number("Replies", 5192),
        isClosed: boolean("Closed", false),
        startedAt: "2020-05-01T10:49:02.159Z",
        lastPostedAt: "2020-05-02T12:38:41.159Z",
        starterName: "LoremIpsum",
        lastPosterName: "DolorMet",
        starter: userFactory({ username: "DolorMet" }),
        lastPoster: userFactory({ username: "DolorMet" }),
        category: Object.assign({}, categories[0], {
          parent: boolean("In child category", true) ? categories[1] : null,
        }),
      }}
    />
  </RootContainer>
)

export const ThreadByAnonymous = () => (
  <RootContainer padding>
    <ThreadHeader
      acl={{ edit: false }}
      moderation={null}
      thread={{
        id: "1",
        title: text(
          "Title",
          "First observed by the astronomer Galileo Galilei!"
        ),
        slug: "test-slug",
        replies: number("Replies", 5192),
        isClosed: boolean("Closed", false),
        startedAt: "2020-05-01T10:49:02.159Z",
        lastPostedAt: "2020-05-02T12:38:41.159Z",
        starterName: "LoremIpsum",
        lastPosterName: "DolorMet",
        starter: null,
        lastPoster: null,
        category: Object.assign({}, categories[0], {
          parent: boolean("In child category", true) ? categories[1] : null,
        }),
      }}
    />
  </RootContainer>
)

export const ThreadEditable = () => (
  <MockedProvider>
    <RootContainer padding>
      <ThreadHeader
        acl={{ edit: true }}
        moderation={null}
        thread={{
          id: "1",
          title: text(
            "Title",
            "First observed by the astronomer Galileo Galilei!"
          ),
          slug: "test-slug",
          replies: number("Replies", 5192),
          isClosed: boolean("Closed", false),
          startedAt: "2020-05-01T10:49:02.159Z",
          lastPostedAt: "2020-05-02T12:38:41.159Z",
          starterName: "LoremIpsum",
          lastPosterName: "DolorMet",
          starter: userFactory({ username: "DolorMet" }),
          lastPoster: userFactory({ username: "DolorMet" }),
          category: Object.assign({}, categories[0], {
            parent: boolean("In child category", true) ? categories[1] : null,
          }),
        }}
      />
    </RootContainer>
  </MockedProvider>
)

export const ThreadWithModeration = () => {
  const closed = boolean("Closed", false)

  const closeThread = () => {}
  const openThread = () => {}
  const moveThread = () => {}
  const deleteThread = () => {}

  return (
    <MockedProvider>
      <RootContainer padding>
        <ThreadHeader
          acl={{ edit: true }}
          moderation={{
            loading: false,
            closeThread,
            openThread,
            moveThread,
            deleteThread,
            actions: [
              {
                name: "Open",
                icon: "unlock",
                iconSolid: true,
                disabled: !closed,
                action: openThread,
              },
              {
                name: "Close",
                icon: "lock",
                iconSolid: true,
                disabled: closed,
                action: closeThread,
              },
              {
                name: "Move",
                icon: "arrow-right",
                iconSolid: true,
                action: moveThread,
              },
              {
                name: "Delete",
                icon: "times",
                iconSolid: true,
                action: deleteThread,
              },
            ],
          }}
          thread={{
            id: "1",
            title: text(
              "Title",
              "First observed by the astronomer Galileo Galilei!"
            ),
            slug: "test-slug",
            replies: number("Replies", 5192),
            isClosed: boolean("Closed", false),
            startedAt: "2020-05-01T10:49:02.159Z",
            lastPostedAt: "2020-05-02T12:38:41.159Z",
            starterName: "LoremIpsum",
            lastPosterName: "DolorMet",
            starter: userFactory({ username: "DolorMet" }),
            lastPoster: userFactory({ username: "DolorMet" }),
            category: Object.assign({}, categories[0], {
              parent: boolean("In child category", true)
                ? categories[1]
                : null,
            }),
          }}
        />
      </RootContainer>
    </MockedProvider>
  )
}
