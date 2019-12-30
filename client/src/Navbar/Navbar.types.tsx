import { IAvatar } from "../types"

export interface INavbarProps {
  settings: INavbarSettingsProp
  user: INavbarUserProp | null
}

export interface INavbarSettingsProp {
  forumName: string
}

export interface INavbarUserProp {
  id: string
  name: string
  avatars: Array<IAvatar>
}
