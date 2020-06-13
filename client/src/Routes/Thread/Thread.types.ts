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
  banner: { full: ICategoryBanner; half: ICategoryBanner } | null
}

export interface IThreadPoster {
  id: string
  name: string
  slug: string
  avatars: Array<IAvatar>
}
