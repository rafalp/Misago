// Frequently used types and types for data loaded on app's start
export type MutationError = {
  location: Array<string>
  message: string
  type: string
}

export type AvatarData = {
  size: number
  url: string
}

export interface AuthUser {
  id: string
  name: string
  slug: string
  email: string | null
  isModerator: boolean
  isAdministrator: boolean
  joinedAt: string
  avatars: Array<AvatarData>
  extra: any
}

export interface ICategory {
  id: string
  parent: ICategory | null
  children: Array<ICategory>
  depth: number
  name: string
  slug: string
  color: string | null
  icon: string | null
  banner: { full: ICategoryBanner; half: ICategoryBanner } | null
  threads: number
  posts: number
  isClosed: boolean
}

export interface ICategoryBanner {
  align: string
  background: string
  height: number
  url: string
}

export type Settings = {
  bulkActionLimit: number
  enableSiteWizard: boolean
  forumIndexHeader: string
  forumIndexThreads: boolean
  forumIndexTitle: string
  forumName: string
  passwordMinLength: number
  passwordMaxLength: number
  postMinLength: number
  threadTitleMinLength: number
  threadTitleMaxLength: number
  usernameMinLength: number
  usernameMaxLength: number
}

export interface ForumStats {
  id: string
  threads: number
  posts: number
  users: number
}

export enum AuthModalMode {
  LOGIN,
  REGISTER,
}

export type RichTextParagraph = {
  id: string
  type: string
  text: string
}

export type RichTextNode = RichTextParagraph

export type RichText = Array<RichTextNode>
