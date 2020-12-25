import { Trans } from "@lingui/macro"
import React from "react"
import { useAuthContext, useModalContext } from "../../../Context"
import { Post, Thread } from "../Thread.types"
import { PostsModeration } from "./ThreadPostsModeration.types"
import ThreadPostsModerationDelete from "./ThreadPostsModerationDelete"

const useThreadPostsModeration = (
  thread: Thread | null,
  posts: Array<Post>,
  page: number | undefined
): PostsModeration | null => {
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
        icon: "fas fa-times",
        action: deletePosts,
      },
    ],
  }
}

export default useThreadPostsModeration
