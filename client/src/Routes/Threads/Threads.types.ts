import { IAvatar, ICategory } from "../../types"

export interface IActiveCategory {
  category: ICategory
  parent: ICategory
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
  avatars: Array<IAvatar>
}

export interface IThreadsModeration {
  actions: Array<IThreadsModerationAction>
  disabled: boolean
  loading: boolean
  closeThreads: () => void
  openThreads: () => void
  moveThreads: () => void
  deleteThreads: () => void
}

export interface IThreadsModerationAction {
  name: React.ReactNode
  icon: string
  iconSolid?: boolean
  action: () => Promise<void> | void
}

export interface ISelectedThread {
  id: string
  title: string
  replies: number
  category: IThreadCategory
}
