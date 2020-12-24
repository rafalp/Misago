// Frequently used interfaces and interfaces for data loaded on app's start
export interface MutationError {
  location: Array<string>
  message: string
  type: string
}

export interface AvatarData {
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

export interface Category {
  id: string
  parent: Category | null
  children: Array<Category>
  depth: number
  name: string
  slug: string
  color: string | null
  icon: string | null
  banner: { full: CategoryBanner; half: CategoryBanner } | null
  threads: number
  posts: number
  isClosed: boolean
}

export interface CategoryBanner {
  align: string
  background: string
  height: number
  url: string
}

export interface Settings {
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

export interface RichTextParagraph {
  id: string
  type: string
  text: string
}

export type RichTextNode = RichTextParagraph

export type RichText = Array<RichTextNode>
