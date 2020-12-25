import React from "react"

export interface PostsModeration {
  actions: Array<PostsModerationAction>
  loading: boolean
}

export interface PostsModerationAction {
  name: React.ReactNode
  icon: string
  action: () => Promise<void> | void
}
