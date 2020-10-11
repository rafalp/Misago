import { IThreadModeration } from "../Thread.types"

export interface IThreadToolbarProps {
  isClosed?: boolean
  moderation?: IThreadModeration | null
  pagination: {
    page: number
    pages: number
    url: (page: number) => string
  }
}
