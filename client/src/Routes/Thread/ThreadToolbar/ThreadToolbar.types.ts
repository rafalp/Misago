import { ThreadModerationOptions } from "../Thread.types"

export interface ThreadToolbarProps {
  isClosed?: boolean
  moderation?: ThreadModerationOptions | null
  pagination: {
    page: number
    pages: number
    url: (page: number) => string
  }
}
