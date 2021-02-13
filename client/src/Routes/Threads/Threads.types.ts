import { AvatarData, Category } from "../../types"

export interface ActiveCategory {
  category: Category
  parent: Category
}

export interface CategoryAcl {
  start: boolean
}

export interface Thread {
  id: string
  category: ThreadCategory
  starter: ThreadPoster | null
  starterName: string
  lastPoster: ThreadPoster | null
  lastPosterName: string
  title: string
  slug: string
  startedAt: string
  lastPostedAt: string
  replies: number
  isClosed: boolean
}

export interface ThreadCategory {
  id: string
  name: string
  slug: string
  color: string | null
  icon: string | null
  parent: ThreadCategory | null
}

export interface ThreadPoster {
  id: string
  name: string
  slug: string
  avatars: Array<AvatarData>
}

export interface ThreadsModerationOptions {
  actions: Array<ThreadsModerationAction>
  disabled: boolean
  loading: boolean
}

export interface ThreadsModerationAction {
  name: React.ReactNode
  icon: string
  action: () => Promise<void> | void
}

export interface SelectedThread {
  id: string
  title: string
  replies: number
  category: ThreadCategory
}
