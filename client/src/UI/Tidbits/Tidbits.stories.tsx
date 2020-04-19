import React from "react"
import { CardContainer } from "../Storybook"
import {
  TidbitItem,
  TidbitMembers,
  TidbitPosts,
  TidbitThreads,
  Tidbits,
} from "."

export default {
  title: "UI/Tidbits",
}

export const Item = () => {
  return (
    <CardContainer padding>
      <Tidbits>
        <TidbitItem>Lorem ipsum</TidbitItem>
        <TidbitItem>Dolor met</TidbitItem>
      </Tidbits>
    </CardContainer>
  )
}

export const PostsThreadsMembers = () => {
  return (
    <CardContainer padding>
      <Tidbits>
        <TidbitPosts value={142567} />
        <TidbitThreads value={1089524} />
        <TidbitMembers value={25663} />
      </Tidbits>
    </CardContainer>
  )
}
