export interface IAvatar {
  size: number
  url: string
}

export interface IUser {
  id: string
  name: string
  slug: string
  email: string | null
  isModerator: boolean
  isAdministrator: boolean
  joinedAt: string
  avatars: Array<IAvatar>
  extra: any
}

export interface ICategory {
    id: string
    parent: ICategory | null
    children: Array<ICategory>
    depth: number
    name: string
    slug: string
    color: string
}

export interface ISettings {
  forumName: string
}