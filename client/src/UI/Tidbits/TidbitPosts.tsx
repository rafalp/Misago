import { Plural, Trans } from "@lingui/macro"
import React from "react"
import TidbitItem from "./TidbitItem"
import TidbitNumber from "./TidbitNumber"

interface ITidbitPostsProps {
  posts: number
}

const TidbitPosts: React.FC<ITidbitPostsProps> = ({ posts }) => (
  <TidbitItem className="tidbit-posts">
    <Plural
      id="tidbit.posts"
      value={posts}
      one={<Trans><TidbitNumber>#</TidbitNumber> post</Trans>}
      other={<Trans><TidbitNumber>#</TidbitNumber> posts</Trans>}
    />
  </TidbitItem>
)

export default TidbitPosts