import React from "react"
import { RootContainer } from "../../../UI/Storybook"
import ThreadToolbarBottom from "./ThreadToolbarBottom"
import ThreadToolbarTop from "./ThreadToolbarTop"

export default {
  title: "Route/Thread/Toolbars",
}

const url = (page: number) => {
  if (page > 1) return `/thread/${page}/`
  return "/thread/"
}

export const Default = () => (
  <RootContainer padding>
    <ThreadToolbarTop paginatorUrl={url} />
    <hr />
    <ThreadToolbarBottom paginatorUrl={url} />
  </RootContainer>
)
