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
  posts: IThreadPosts
  extra: Record<string, any>
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

export interface IPost {
  id: string
  poster: IPoster | null
  posterName: string
  body: { text: string }
  edits: number
  postedAt: string
  extra: Record<string, any>
}

export interface IPoster {
  id: string
  name: string
  slug: string
  avatars: Array<IAvatar>
  extra: Record<string, any>
}

export interface IThreadPosts {
  page: IThreadPostsPage | null
  pagination: {
    pages: number
  }
}

export interface IThreadPostsPage {
  items: Array<IPost>
  number: number
  start: number
  stop: number
}

export interface IPostsModeration {
  actions: Array<IPostsModerationAction>
  disabled: boolean
  loading: boolean
  deletePosts: () => void
}

export interface IPostsModerationAction {
  name: React.ReactNode
  icon: string
  iconSolid?: boolean
  action: () => Promise<void> | void
}