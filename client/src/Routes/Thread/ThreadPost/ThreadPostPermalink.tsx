import { Trans } from "@lingui/macro"
import React from "react"
import { useToastsContext } from "../../../Context"
import { DropdownLink } from "../../../UI/Dropdown"
import * as urls from "../../../urls"
import { Post } from "../Thread.types"

interface ThreadPostPermalinkProps {
  post: Post
  threadId: string
  threadSlug: string
}

const ThreadPostPermalink: React.FC<ThreadPostPermalinkProps> = ({
  post,
  threadId,
  threadSlug,
}) => {
  const { showToast } = useToastsContext()

  return (
    <DropdownLink
      to={urls.threadPost({ id: threadId, slug: threadSlug }, post)}
      text={<Trans id="post.permalink">Permalink</Trans>}
      icon="fas fa-link"
      onClick={(event) => {
        if (navigator?.clipboard?.writeText && window.URL) {
          navigator.clipboard.writeText(
            new URL(
              urls.threadPost({ id: threadId, slug: threadSlug }, post),
              document.baseURI
            ).href
          )
          showToast(
            <Trans id="post.permalink_copied">
              Post link copied to the clipboard.
            </Trans>
          )
          event.preventDefault()
        }
      }}
    />
  )
}

export default ThreadPostPermalink
