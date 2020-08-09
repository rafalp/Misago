import { withKnobs, boolean } from "@storybook/addon-knobs"
import React from "react"
import { RootContainer } from "../../../UI/Storybook"
import ThreadToolbarBottom from "./ThreadToolbarBottom"
import ThreadToolbarTop from "./ThreadToolbarTop"

export default {
  title: "Route/Thread/Toolbars",
  decorators: [withKnobs],
}

const url = (page: number) => {
  if (page > 1) return `/thread/${page}/`
  return "/thread/"
}

export const Default = () => {
  const props = {
    pagination: {
      url,
      page: 1,
      pages: 1,
    },
  }

  return (
    <RootContainer padding>
      <ThreadToolbarTop {...props} />
      <hr />
      <ThreadToolbarBottom {...props} />
    </RootContainer>
  )
}

export const WithPages = () => {
  const props = {
    pagination: {
      url,
      page: 7,
      pages: 21,
    },
  }

  return (
    <RootContainer padding>
      <ThreadToolbarTop {...props} />
      <hr />
      <ThreadToolbarBottom {...props} />
    </RootContainer>
  )
}

export const WithModeration = () => {
  const props = {
    moderation: {
      loading: boolean("Loading", false),
      closeThread: () => {},
      openThread: () => {},
      moveThread: () => {},
      deleteThread: () => {},
      actions: [],
    },
    pagination: {
      url,
      page: 1,
      pages: 1,
    },
  }

  return (
    <RootContainer padding>
      <ThreadToolbarTop {...props} />
      <hr />
      <ThreadToolbarBottom {...props} />
    </RootContainer>
  )
}

export const WithModerationAndPages = () => {
  const props = {
    moderation: {
      loading: boolean("Loading", false),
      closeThread: () => {},
      openThread: () => {},
      moveThread: () => {},
      deleteThread: () => {},
      actions: [],
    },
    pagination: {
      url,
      page: 7,
      pages: 21,
    },
  }

  return (
    <RootContainer padding>
      <ThreadToolbarTop {...props} />
      <hr />
      <ThreadToolbarBottom {...props} />
    </RootContainer>
  )
}
