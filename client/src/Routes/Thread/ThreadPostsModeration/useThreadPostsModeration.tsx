import { Trans } from "@lingui/macro"
import React from "react"
import { useAuthContext } from "../../../Context"
import { IPost, IPostsModeration, IThread} from "../Thread.types"

const useThreadPostsModeration = (
  thread: IThread, posts: Array<IPost>
): IPostsModeration | null => {
  const user = useAuthContext()

  const deletePosts = () => {}

  const moderation = {
    loading: false,
    disabled: posts.length === 0,
    deletePosts,
    actions: [
      {
        name: <Trans id="moderation.delete">Delete</Trans>,
        icon: "times",
        iconSolid: true,
        action: deletePosts,
      },
    ],
  }

  if (user && user.isModerator) return moderation
  return null
}

export default useThreadPostsModeration