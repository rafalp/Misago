import React from "react"
import { RootContainer } from "../Storybook"
import Paginator from "./Paginator"

export default {
  title: "UI/Paginator",
}

const url = (page: number) => {
  if (page > 1) return `/somewhere/${page}/`
  return "/somewhere/"
}

export const FirstPage = () => (
  <RootContainer padding>
    <Paginator page={1} pages={10} url={url} />
  </RootContainer>
)

export const MiddlePage = () => (
  <RootContainer padding>
    <Paginator page={5} pages={10} url={url} />
  </RootContainer>
)

export const LastPage = () => (
  <RootContainer padding>
    <Paginator page={10} pages={10} url={url} />
  </RootContainer>
)

export const OnlyPage = () => (
  <RootContainer padding>
    <Paginator page={1} pages={1} url={url} />
  </RootContainer>
)
