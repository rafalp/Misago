import { action } from "@storybook/addon-actions"
import { withKnobs, boolean } from "@storybook/addon-knobs"
import { ApolloError } from "apollo-client"
import React from "react"
import { ModalContainer, categories } from "../../../../UI/Storybook"
import ThreadsModerationError from "./ThreadsModerationError"

export default {
  title: "Route/Threads/Moderation/Error",
  decorators: [withKnobs],
}

const close = action("close modal")

const threads = [
  {
    id: "1",
    title: "Nam id ante ultricies, laoreet leo tempor, venenatis ipsum.",
    replies: 719,
    category: Object.assign({}, categories[0].children[2], {
      parent: categories[0],
    }),
  },
  {
    id: "2",
    title: "Donec in tempor tellus.",
    replies: 0,
    category: Object.assign({}, categories[2]),
  },
]

export const AuthError = () => (
  <ModalContainer>
    <ThreadsModerationError
      errors={[
        {
          location: ["threads", "0"],
          message: "moderator permission is required",
          type: "auth_error.not_moderator",
        },
        {
          location: ["threads", "1"],
          message: "moderator permission is required",
          type: "auth_error.not_moderator",
        },
        {
          location: ["__root__"],
          type: "auth_error.not_authorized",
          message: "authorization is required",
        },
      ]}
      threads={threads}
      forDelete={boolean("For delete", false)}
      close={close}
    />
  </ModalContainer>
)

export const ThreadsErrors = () => (
  <ModalContainer>
    <ThreadsModerationError
      errors={[
        {
          location: ["threads", "0"],
          message: "moderator permission is required",
          type: "auth_error.not_moderator",
        },
        {
          location: ["threads", "1"],
          message: "moderator permission is required",
          type: "auth_error.not_moderator",
        },
      ]}
      threads={threads}
      forDelete={boolean("For delete", false)}
      close={close}
    />
  </ModalContainer>
)

export const SomeThreadsErrors = () => (
  <ModalContainer>
    <ThreadsModerationError
      errors={[
        {
          location: ["threads", "1"],
          message: "moderator permission is required",
          type: "auth_error.not_moderator",
        },
      ]}
      threads={threads}
      forDelete={boolean("For delete", false)}
      close={close}
    />
  </ModalContainer>
)

export const QueryError = () => (
  <ModalContainer>
    <ThreadsModerationError
      graphqlError={new ApolloError({})}
      forDelete={boolean("For delete", false)}
      close={close}
    />
  </ModalContainer>
)

export const NetworkError = () => (
  <ModalContainer>
    <ThreadsModerationError
      graphqlError={new ApolloError({ networkError: new Error() })}
      forDelete={boolean("For delete", false)}
      close={close}
    />
  </ModalContainer>
)
