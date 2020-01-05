import { IAvatar } from "../types"

export interface INavbarProps {
  openRegister: () => void
  settings?: INavbarSettingsProp | null
  user?: INavbarUserProp | null
}

export interface INavbarSettingsProp {
  forumName: string
}

export interface INavbarUserProp {
  id: string
  name: string
  avatars: Array<IAvatar>
}
