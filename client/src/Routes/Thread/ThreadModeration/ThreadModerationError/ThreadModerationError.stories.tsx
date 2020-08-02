import { action } from "@storybook/addon-actions"
import { withKnobs, boolean } from "@storybook/addon-knobs"
import { ApolloError } from "apollo-client"
import React from "react"
import { ModalContainer } from "../../../../UI/Storybook"
import ThreadModerationError from "./ThreadModerationError"

export default {
  title: "Route/Thread/Moderation/Thread Error",
  decorators: [withKnobs],
}

const close = action("close modal")

export const AuthError = () => (
  <ModalContainer>
    <ThreadModerationError
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
    <ThreadModerationError
      errors={[
        {
          location: ["thread"],
          message: "moderator permission is required",
          type: "auth_error.not_moderator",
        },
      ]}
      forDelete={boolean("For delete", false)}
      close={close}
    />
  </ModalContainer>
)

export const QueryError = () => (
  <ModalContainer>
    <ThreadModerationError
      graphqlError={new ApolloError({})}
      forDelete={boolean("For delete", false)}
      close={close}
    />
  </ModalContainer>
)

export const NetworkError = () => (
  <ModalContainer>
    <ThreadModerationError
      graphqlError={new ApolloError({ networkError: new Error() })}
      forDelete={boolean("For delete", false)}
      close={close}
    />
  </ModalContainer>
)
