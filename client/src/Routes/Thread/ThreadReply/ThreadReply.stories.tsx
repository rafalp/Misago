import { MockedProvider } from "@apollo/react-testing"
import React from "react"
import { ButtonPrimary, ButtonSecondary } from "../../../UI/Button"
import { RootContainer, SettingsContextFactory } from "../../../UI/Storybook"
import ThreadReply from "./ThreadReply"
import { ThreadReplyContext, ThreadReplyProvider } from "./ThreadReplyContext"

export default {
  title: "Route/Thread/Reply Form",
}

export const NewReplyForm = () => (
  <SettingsContextFactory>
    <MockedProvider>
      <ThreadReplyProvider active>
        <ThreadReply threadId="1" />
      </ThreadReplyProvider>
    </MockedProvider>
  </SettingsContextFactory>
)

export const HiddenForm = () => (
  <SettingsContextFactory>
    <MockedProvider>
      <ThreadReplyProvider>
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
                    onClick={value.deactivate}
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

export const CrashedReplyForm = () => (
  <MockedProvider>
    <ThreadReplyProvider active>
      <ThreadReply threadId="1" />
    </ThreadReplyProvider>
  </MockedProvider>
)
