import { IAvatar, ICategoryBanner } from "../../types"

export interface IThread {
  id: string
  slug: string
  title: string
  startedAt: string
  lastPostedAt: string
  replies: number
  starterName: string
  lastPosterName: string
  isClosed: boolean
  starter: IThreadPoster | null
  lastPoster: IThreadPoster | null
  category: IThreadCategory
}

export interface IThreadCategory {
  id: string
  name: string
  slug: string
  parent: IThreadCategory | null
  color: string | null
  isClosed: boolean
  banner: { full: ICategoryBanner; half: ICategoryBanner } | null
}

export interface IThreadPoster {
  id: string
  name: string
  slug: string
  avatars: Array<IAvatar>
}

export interface IThreadModeration {
  actions: Array<IThreadModerationAction>
  loading: boolean
  closeThread: () => void
  openThread: () => void
  moveThread: () => void
  deleteThread: () => void
}

export interface IThreadModerationAction {
  name: React.ReactNode
  icon: string
  iconSolid?: boolean
  disabled?: boolean
  action: () => Promise<void> | void
}
