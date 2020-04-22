import { action } from "@storybook/addon-actions"
import React from "react"
import { RootContainer } from "../Storybook"
import LoadMoreButton from "./LoadMoreButton"

export default {
  title: "UI/LoadMoreButton",
}

const event = action("load more")
const data = { nextCursor: "next" }

export const Default = () => (
  <RootContainer padding>
    <LoadMoreButton
      data={data}
      loading={false}
      onEvent={event}
    />
  </RootContainer>
)

export const Loading = () => (
  <RootContainer padding>
    <LoadMoreButton
      data={data}
      loading={true}
      onEvent={event}
    />
  </RootContainer>
)

export const NoCursor = () => (
  <RootContainer padding>
    <LoadMoreButton
      data={{ nextCursor: null }}
      loading={false}
      onEvent={event}
    />
  </RootContainer>
)

export const NoData = () => (
  <RootContainer padding>
    <LoadMoreButton
      data={null}
      loading={false}
      onEvent={event}
    />
  </RootContainer>
)
