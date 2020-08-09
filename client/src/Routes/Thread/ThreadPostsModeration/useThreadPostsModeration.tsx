import { Trans } from "@lingui/macro"
import React from "react"
import { useAuthContext, useModalContext } from "../../../Context"
import { IPost, IThread } from "../Thread.types"
import { IPostsModeration } from "./ThreadPostsModeration.types"
import ThreadPostsModerationDelete from "./ThreadPostsModerationDelete"

const useThreadPostsModeration = (
  thread: IThread | null,
  posts: Array<IPost>,
  page: number | undefined
): IPostsModeration | null => {
  const user = useAuthContext()
  const { openModal } = useModalContext()

  if (!thread || !user || !user.isModerator) return null

  const deletePosts = () => {
    openModal(
      <ThreadPostsModerationDelete thread={thread} posts={posts} page={page} />
    )
  }

  return {
    loading: false,
    actions: [
      {
        name: <Trans id="moderation.delete">Delete</Trans>,
        icon: "times",
        iconSolid: true,
        action: deletePosts,
      },
    ],
  }
}

export default useThreadPostsModeration
