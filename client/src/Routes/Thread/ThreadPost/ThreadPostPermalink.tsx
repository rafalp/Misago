import { Trans } from "@lingui/macro"
import React from "react"
import { useToastsContext } from "../../../Context"
import { DropdownLink } from "../../../UI"
import * as urls from "../../../urls"
import { IPost } from "../Thread.types"

interface IThreadPostPermalinkProps {
  post: IPost
  threadId: string
  threadSlug: string
}

const ThreadPostPermalink: React.FC<IThreadPostPermalinkProps> = ({
  post,
  threadId,
  threadSlug,
}) => {
  const { showToast } = useToastsContext()

  return (
    <DropdownLink
      to={urls.threadPost({ id: threadId, slug: threadSlug }, post)}
      icon="link"
      iconSolid
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
    >
      <Trans id="post.permalink">Permalink</Trans>
    </DropdownLink>
  )
}

export default ThreadPostPermalink
