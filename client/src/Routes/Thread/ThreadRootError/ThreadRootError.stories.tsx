import { withKnobs, select } from "@storybook/addon-knobs"
import { ApolloError } from "apollo-client"
import React from "react"
import { RootContainer } from "../../../UI/Storybook"
import ThreadRootError from "./ThreadRootError"

export default {
  title: "Route/Thread/Thread RootError",
  decorators: [withKnobs],
}

export const ThreadError = () => (
  <RootContainer>
    <ThreadRootError
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
    </ThreadRootError>
  </RootContainer>
)

export const QueryError = () => (
  <RootContainer>
    <ThreadRootError graphqlError={new ApolloError({})}>
      {({ message }) => <p>{message}</p>}
    </ThreadRootError>
  </RootContainer>
)

export const NetworkError = () => (
  <RootContainer>
    <ThreadRootError
      graphqlError={new ApolloError({ networkError: new Error() })}
    >
      {({ message }) => <p>{message}</p>}
    </ThreadRootError>
  </RootContainer>
)
