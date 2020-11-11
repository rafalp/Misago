import { withKnobs, select } from "@storybook/addon-knobs"
import { ApolloError } from "apollo-client"
import React from "react"
import { RootContainer } from "../../../../UI/Storybook"
import ThreadReplyRootError from "./ThreadReplyRootError"

export default {
  title: "Route/Thread/Reply Form/Root Error",
  decorators: [withKnobs],
}

export const PostError = () => (
  <RootContainer>
    <ThreadReplyRootError
      dataErrors={[
        {
          location: ["post"],
          message: "moderator permission is required",
          type: select(
            "Error",
            {
              "Not moderator": "auth_error.not_moderator",
              "Category is closed": "auth_error.category.closed",
              "Thread is closed": "auth_error.thread.closed",
              "Post not author": "auth_error.post.not_author",
              "Post not found": "value_error.post.not_exists",
            },
            "auth_error.not_moderator"
          ),
        },
      ]}
    >
      {({ message }) => <p>{message}</p>}
    </ThreadReplyRootError>
  </RootContainer>
)

export const ThreadError = () => (
  <RootContainer>
    <ThreadReplyRootError
      dataErrors={[
        {
          location: ["thread"],
          message: "moderator permission is required",
          type: select(
            "Error",
            {
              "Not moderator": "auth_error.not_moderator",
              "Category is closed": "auth_error.category.closed",
              "Thread is closed": "auth_error.thread.closed",
              "Thread not author": "auth_error.thread.not_author",
              "Thread not found": "value_error.thread.not_exists",
            },
            "auth_error.not_moderator"
          ),
        },
      ]}
    >
      {({ message }) => <p>{message}</p>}
    </ThreadReplyRootError>
  </RootContainer>
)

export const QueryError = () => (
  <RootContainer>
    <ThreadReplyRootError graphqlError={new ApolloError({})}>
      {({ message }) => <p>{message}</p>}
    </ThreadReplyRootError>
  </RootContainer>
)

export const NetworkError = () => (
  <RootContainer>
    <ThreadReplyRootError
      graphqlError={new ApolloError({ networkError: new Error() })}
    >
      {({ message }) => <p>{message}</p>}
    </ThreadReplyRootError>
  </RootContainer>
)
