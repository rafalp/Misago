import { number, withKnobs } from "@storybook/addon-knobs"
import React from "react"
import { RootContainer } from "../Storybook"
import Paginator from "./Paginator"
import PaginatorCompact from "./PaginatorCompact"

export default {
  title: "UI/Paginator",
  decorators: [withKnobs],
}

const url = (page: number) => {
  if (page > 1) return `/somewhere/${page}/`
  return "/somewhere/"
}

export const FirstPage = () => (
  <RootContainer>
    <Paginator page={1} pages={10} url={url} />
    <hr />
    <PaginatorCompact page={1} pages={10} url={url} />
  </RootContainer>
)

export const MiddlePage = () => (
  <RootContainer>
    <Paginator page={5} pages={10} url={url} />
    <hr />
    <PaginatorCompact page={5} pages={10} url={url} />
  </RootContainer>
)

export const LastPage = () => (
  <RootContainer>
    <Paginator page={10} pages={10} url={url} />
    <hr />
    <PaginatorCompact page={10} pages={10} url={url} />
  </RootContainer>
)

export const OnlyPage = () => (
  <RootContainer>
    <Paginator page={1} pages={1} url={url} />
    <hr />
    <PaginatorCompact page={1} pages={1} url={url} />
  </RootContainer>
)

export const Configurable = () => {
  let page = number("Page", 1)
  let pages = number("Pages", 10)

  if (page < 1) page = 1
  if (pages < page) pages = page

  return (
    <RootContainer>
      <Paginator page={page} pages={pages} url={url} />
      <hr />
      <PaginatorCompact page={page} pages={pages} url={url} />
    </RootContainer>
  )
}
