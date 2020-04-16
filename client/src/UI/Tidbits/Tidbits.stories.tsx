import React from "react"
import { CardContainer } from "../Storybook"
import { TidbitItem, TidbitPosts, TidbitThreads, Tidbits } from "."

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

export const PostsThreads = () => {
  return (
    <CardContainer padding>
      <Tidbits>
        <TidbitPosts posts={71315} />
        <TidbitThreads threads={22453} />
      </Tidbits>
    </CardContainer>
  )
}
