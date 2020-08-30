import { IAvatar } from "../types"

export interface INavbarProps {
  settings?: INavbarSettingsProp | null
  user?: INavbarUserProp | null
}

export interface INavbarSettingsProp {
  forumName: string
  forumIndexThreads: boolean
}

export interface INavbarUserProp {
  id: string
  name: string
  slug: string
  avatars: Array<IAvatar>
}
