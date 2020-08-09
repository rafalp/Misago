import { action } from "@storybook/addon-actions"
import { withKnobs, boolean } from "@storybook/addon-knobs"
import { ApolloError } from "apollo-client"
import React from "react"
import { ModalContainer } from "../../../../../UI/Storybook"
import ThreadPostModerationError from "./ThreadPostModerationError"

export default {
  title: "Route/Thread/Moderation/Post Error",
  decorators: [withKnobs],
}

const close = action("close modal")

export const AuthError = () => (
  <ModalContainer>
    <ThreadPostModerationError
      errors={[
        {
          location: ["post"],
          message: "moderator permission is required",
          type: "auth_error.not_moderator",
        },
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
    <ThreadPostModerationError
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

export const PostError = () => (
  <ModalContainer>
    <ThreadPostModerationError
      errors={[
        {
          location: ["post"],
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
    <ThreadPostModerationError
      graphqlError={new ApolloError({})}
      forDelete={boolean("For delete", false)}
      close={close}
    />
  </ModalContainer>
)

export const NetworkError = () => (
  <ModalContainer>
    <ThreadPostModerationError
      graphqlError={new ApolloError({ networkError: new Error() })}
      forDelete={boolean("For delete", false)}
      close={close}
    />
  </ModalContainer>
)
