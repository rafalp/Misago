import React from "react"

export interface IPostsModeration {
  actions: Array<IPostsModerationAction>
  loading: boolean
  deletePosts: () => void
}

export interface IPostsModerationAction {
  name: React.ReactNode
  icon: string
  iconSolid?: boolean
  action: () => Promise<void> | void
}
