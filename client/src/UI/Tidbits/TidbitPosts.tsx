import { Plural, Trans } from "@lingui/macro"
import React from "react"
import TidbitItem from "./TidbitItem"
import TidbitNumber from "./TidbitNumber"

interface ITidbitPostsProps {
  value: number
}

const TidbitPosts: React.FC<ITidbitPostsProps> = ({ value }) => (
  <TidbitItem className="tidbit-posts">
    <Plural
      id="tidbit.posts"
      value={value}
      one={
        <Trans>
          <TidbitNumber>#</TidbitNumber> post
        </Trans>
      }
      other={
        <Trans>
          <TidbitNumber>#</TidbitNumber> posts
        </Trans>
      }
    />
  </TidbitItem>
)

export default TidbitPosts
