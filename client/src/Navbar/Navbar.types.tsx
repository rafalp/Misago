import { AvatarData } from "../types"

export interface NavbarProps {
  settings?: Settings | null
  user?: User | null
}

export interface Settings {
  forumName: string
  forumIndexThreads: boolean
}

export interface User {
  id: string
  name: string
  slug: string
  avatars: Array<AvatarData>
}
