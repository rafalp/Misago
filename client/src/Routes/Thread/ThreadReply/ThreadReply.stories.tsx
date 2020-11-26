import { MockedProvider } from "@apollo/react-testing"
import { GraphQLError } from "graphql"
import React from "react"
import { ButtonPrimary, ButtonSecondary } from "../../../UI/Button"
import { PostingForm } from "../../../UI/PostingForm"
import { RootContainer, SettingsContextFactory } from "../../../UI/Storybook"
import ThreadReply from "./ThreadReply"
import { ThreadReplyContext, ThreadReplyProvider } from "./ThreadReplyContext"
import ThreadReplyError from "./ThreadReplyError"
import { POST_MARKUP_QUERY } from "./usePostMarkupQuery"

export default {
  title: "Route/Thread/Reply Form",
}

export const NewReplyForm = () => (
  <SettingsContextFactory>
    <MockedProvider>
      <ThreadReplyProvider threadId="1" active>
        <ThreadReply threadId="1" />
      </ThreadReplyProvider>
    </MockedProvider>
  </SettingsContextFactory>
)

export const EditReplyForm = () => (
  <SettingsContextFactory>
    <MockedProvider
      mocks={[
        {
          request: {
            query: POST_MARKUP_QUERY,
            variables: {
              id: "1",
            },
          },
          result: {
            data: {
              post: {
                __typename: "Post",
                id: "1",
                markup: "Hello world!",
                richText: [],
              },
            },
          },
        },
      ]}
    >
      <ThreadReplyProvider threadId="1" mode="edit" post={{ id: "1" }} active>
        <ThreadReply threadId="1" />
      </ThreadReplyProvider>
    </MockedProvider>
  </SettingsContextFactory>
)

export const EditReplyNotFoundError = () => (
  <SettingsContextFactory>
    <MockedProvider
      mocks={[
        {
          request: {
            query: POST_MARKUP_QUERY,
            variables: {
              id: "1",
            },
          },
          result: {
            data: {
              post: null,
            },
          },
        },
      ]}
    >
      <ThreadReplyProvider threadId="1" mode="edit" post={{ id: "1" }} active>
        <ThreadReply threadId="1" />
      </ThreadReplyProvider>
    </MockedProvider>
  </SettingsContextFactory>
)

export const EditReplyNetworkError = () => (
  <SettingsContextFactory>
    <MockedProvider
      mocks={[
        {
          request: {
            query: POST_MARKUP_QUERY,
            variables: {
              id: "1",
            },
          },
          error: new Error("Test error"),
        },
      ]}
    >
      <ThreadReplyProvider threadId="1" mode="edit" post={{ id: "1" }} active>
        <ThreadReply threadId="1" />
      </ThreadReplyProvider>
    </MockedProvider>
  </SettingsContextFactory>
)

export const EditReplyGraphQLError = () => (
  <SettingsContextFactory>
    <MockedProvider
      mocks={[
        {
          request: {
            query: POST_MARKUP_QUERY,
            variables: {
              id: "1",
            },
          },
          result: {
            errors: [new GraphQLError("Test error")],
          },
        },
      ]}
    >
      <ThreadReplyProvider threadId="1" mode="edit" post={{ id: "1" }} active>
        <ThreadReply threadId="1" />
      </ThreadReplyProvider>
    </MockedProvider>
  </SettingsContextFactory>
)

export const HiddenForm = () => (
  <SettingsContextFactory>
    <MockedProvider>
      <ThreadReplyProvider threadId="1">
        <RootContainer>
          <ThreadReplyContext.Consumer>
            {(value) =>
              value && (
                <>
                  <ButtonPrimary
                    text="Open form"
                    disabled={value.isActive}
                    onClick={value.startReply}
                  />{" "}
                  <ButtonSecondary
                    text="Close form"
                    disabled={!value.isActive}
                    onClick={value.cancelReply}
                  />
                </>
              )
            }
          </ThreadReplyContext.Consumer>
        </RootContainer>
        <ThreadReply threadId="1" />
      </ThreadReplyProvider>
    </MockedProvider>
  </SettingsContextFactory>
)

export const ReplyFormError = () => (
  <SettingsContextFactory>
    <MockedProvider>
      <ThreadReplyProvider threadId="1" active>
        <ThreadReplyContext.Consumer>
          {(value) => (
            <PostingForm
              fullscreen={value?.fullscreen}
              minimized={value?.minimized}
              show={value?.isActive}
            >
              <ThreadReplyError />
            </PostingForm>
          )}
        </ThreadReplyContext.Consumer>
      </ThreadReplyProvider>
    </MockedProvider>
  </SettingsContextFactory>
)
