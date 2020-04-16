import { Plural } from "@lingui/macro"
import React from "react"
import TidbitItem from "./TidbitItem"

interface ITidbitPostsProps {
  posts: number
}

const TidbitPosts: React.FC<ITidbitPostsProps> = ({ posts }) => (
  <TidbitItem className="tidbit-posts">
    <Plural
      id="tidbit.posts"
      value={posts}
      one="# post"
      other="# posts"
    />
  </TidbitItem>
)

export default TidbitPosts