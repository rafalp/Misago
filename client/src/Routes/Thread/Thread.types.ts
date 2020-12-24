import { AvatarData, CategoryBanner, RichText } from "../../types"

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
  icon: string | null
  isClosed: boolean
  banner: { full: CategoryBanner; half: CategoryBanner } | null
}

export interface IThreadPoster {
  id: string
  name: string
  slug: string
  avatars: Array<AvatarData>
}

export interface IThreadModeration {
  actions: Array<IModerationAction>
  loading: boolean
}

export interface IModerationAction {
  name: React.ReactNode
  icon: string
  disabled?: boolean
  action: () => Promise<void> | void
}

export interface IPost {
  id: string
  poster: IPoster | null
  posterName: string
  richText: RichText
  edits: number
  postedAt: string
  extra: Record<string, any>
}

export interface IPoster {
  id: string
  name: string
  slug: string
  avatars: Array<AvatarData>
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
