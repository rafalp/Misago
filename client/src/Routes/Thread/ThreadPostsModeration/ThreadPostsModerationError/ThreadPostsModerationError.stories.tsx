import { action } from "@storybook/addon-actions"
import { withKnobs, boolean, text } from "@storybook/addon-knobs"
import React from "react"
import { ModalCloseFooter } from "../../../../UI"
import { ModalContainer, userFactory } from "../../../../UI/Storybook"
import ThreadPostsModerationError from "./ThreadPostsModerationError"

export default {
  title: "Route/Thread/Moderation/Posts Error",
  decorators: [withKnobs],
}

const close = action("close modal")

export const AuthError = () => (
  <ModalContainer>
    <ThreadPostsModerationError
      errors={[
        {
          location: ["posts", "0"],
          message: "moderator permission is required",
          type: "auth_error.not_moderator",
        },
        {
          location: ["posts", "1"],
          message: "moderator permission is required",
          type: "auth_error.not_moderator",
        },
        {
          location: ["__root__"],
          type: "auth_error.not_authorized",
          message: "authorization is required",
        },
      ]}
      selectionErrors={{}}
      posts={[]}
      forDelete={boolean("For delete", false)}
    />
    <ModalCloseFooter close={close} />
  </ModalContainer>
)

export const ThreadError = () => (
  <ModalContainer>
    <ThreadPostsModerationError
      errors={[
        {
          location: ["thread"],
          type: "value_error.thread.not_exists",
          message: "thread not found",
        },
      ]}
      selectionErrors={{}}
      posts={[]}
      forDelete={boolean("For delete", false)}
    />
    <ModalCloseFooter close={close} />
  </ModalContainer>
)

export const PostsErrors = () => {
  const username = text("Username", "JohnSmit")

  return (
    <ModalContainer>
      <ThreadPostsModerationError
        errors={[]}
        selectionErrors={{
          "1": {
            location: ["posts", "0"],
            message: "moderator permission is required",
            type: "auth_error.not_moderator",
          },
          "2": {
            location: ["posts", "1"],
            message: "moderator permission is required",
            type: "auth_error.not_moderator",
          },
        }}
        posts={[
          {
            id: "1",
            body: { text: "Lorem ipsum dolor met sit amet elit." },
            edits: 0,
            postedAt: "2020-04-01T21:42:51Z",
            posterName: username,
            poster: userFactory({ name: username }),
            extra: {},
          },
          {
            id: "2",
            body: {
              text:
                "Aliquam commodo orci et lacinia placerat. Donec non porttitor metus.",
            },
            edits: 0,
            postedAt: "2020-04-02T11:16:51Z",
            posterName: "Lorem",
            poster: userFactory({ name: "Lorem" }),
            extra: {},
          },
        ]}
        forDelete={boolean("For delete", false)}
      />
      <ModalCloseFooter close={close} />
    </ModalContainer>
  )
}
