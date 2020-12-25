import { ThreadModeration } from "../Thread.types"

export interface ThreadToolbarProps {
  isClosed?: boolean
  moderation?: ThreadModeration | null
  pagination: {
    page: number
    pages: number
    url: (page: number) => string
  }
}
