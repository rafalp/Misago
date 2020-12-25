import { Trans } from "@lingui/macro"
import React from "react"
import { useAuthContext, useModalContext } from "../../../../Context"
import { Post } from "../../Thread.types"
import ThreadPostModerationDelete from "./ThreadPostModerationDelete"

const useThreadPostModeration = (
  threadId: string,
  post: Post,
  page: number | undefined
) => {
  const user = useAuthContext()
  const { openModal } = useModalContext()

  if (!user || !user.isModerator) return null

  const deletePost = () =>
    openModal(
      <ThreadPostModerationDelete
        threadId={threadId}
        post={post}
        page={page}
      />
    )

  return {
    deletePost,
    actions: [
      {
        name: <Trans id="moderation.delete">Delete</Trans>,
        icon: "fas fa-times",
        action: deletePost,
      },
    ],
  }
}

export default useThreadPostModeration
