import { action } from "@storybook/addon-actions"
import { withKnobs, boolean, select } from "@storybook/addon-knobs"
import { ApolloError } from "apollo-client"
import React from "react"
import { ModalContainer } from "../../../../UI/Storybook"
import ThreadModerationModalError from "./ThreadModerationModalError"

export default {
  title: "Route/Thread/ThreadModerationErrorModal",
  decorators: [withKnobs],
}

const close = action("close modal")

export const AuthError = () => (
  <ModalContainer>
    <ThreadModerationModalError
      errors={[
        {
          location: ["thread"],
          message: "moderator permission is required",
          type: "auth_error.not_moderator",
        },
        {
          location: ["__root__"],
          type: "auth_error.not_authorized",
          message: "authorization is required",
        },
      ]}
      forDelete={boolean("For delete", false)}
      close={close}
    />
  </ModalContainer>
)

export const ThreadError = () => (
  <ModalContainer>
    <ThreadModerationModalError
      errors={[
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
      forDelete={boolean("For delete", false)}
      close={close}
    />
  </ModalContainer>
)

export const QueryError = () => (
  <ModalContainer>
    <ThreadModerationModalError
      graphqlError={new ApolloError({})}
      forDelete={boolean("For delete", false)}
      close={close}
    />
  </ModalContainer>
)

export const NetworkError = () => (
  <ModalContainer>
    <ThreadModerationModalError
      graphqlError={new ApolloError({ networkError: new Error() })}
      forDelete={boolean("For delete", false)}
      close={close}
    />
  </ModalContainer>
)
