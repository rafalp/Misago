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

export interface RichTextCode {
  id: string
  type: "code"
  syntax: string | null
  text: string
}

export interface RichTextFragment {
  id: string
  type: "f"
  text: string
}

export interface RichTextHeader {
  id: string
  type: "h1" | "h2" | "h3" | "h4" | "h5" | "h6"
  text: string
}

export interface RichTextHorizontalRule {
  id: string
  type: "hr"
}

export interface RichTextList {
  id: string
  type: "list"
  ordered: boolean
  children: RichText
}

export interface RichTextListItem {
  id: string
  type: "li"
  children: Array<RichTextFragment | RichTextList>
}

export interface RichTextParagraph {
  id: string
  type: "p"
  text: string
}

export interface RichTextQuote {
  id: string
  type: "quote"
  children: RichText
}

export type RichTextBlock =
  | RichTextCode
  | RichTextFragment
  | RichTextHeader
  | RichTextHorizontalRule
  | RichTextList
  | RichTextListItem
  | RichTextParagraph
  | RichTextQuote

export type RichText = Array<RichTextBlock>
