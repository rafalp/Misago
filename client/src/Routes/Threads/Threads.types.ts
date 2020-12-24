import { AvatarData, Category } from "../../types"

export interface IActiveCategory {
  category: Category
  parent: Category
}

export interface IThread {
  id: string
  category: IThreadCategory
  starter: IThreadPoster | null
  starterName: string
  lastPoster: IThreadPoster | null
  lastPosterName: string
  title: string
  slug: string
  startedAt: string
  lastPostedAt: string
  replies: number
  isClosed: boolean
}

export interface IThreadCategory {
  id: string
  name: string
  slug: string
  color: string | null
  icon: string | null
  parent: IThreadCategory | null
}

export interface IThreadPoster {
  id: string
  name: string
  slug: string
  avatars: Array<AvatarData>
}

export interface IThreadsModeration {
  actions: Array<IThreadsModerationAction>
  disabled: boolean
  loading: boolean
}

export interface IThreadsModerationAction {
  name: React.ReactNode
  icon: string
  action: () => Promise<void> | void
}

export interface ISelectedThread {
  id: string
  title: string
  replies: number
  category: IThreadCategory
}
