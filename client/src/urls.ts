export const index = () => "/"

interface ISluggable {
  id: string
  slug: string
}

interface IThreadParams extends ISluggable {
  page?: number
}

export const categories = () => `/categories/`
export const category = (category: ISluggable) => {
  return `/c/${category.slug}/${category.id}/`
}
export const startThread = (category?: ISluggable | null) => {
  if (category) return `/start-thread/${category.slug}/${category.id}/`
  return `/start-thread/`
}
export const threads = () => `/threads/`
export const thread = (thread: IThreadParams) => {
  if (thread.page && thread.page > 1) {
    return `/t/${thread.slug}/${thread.id}/${thread.page}/`
  }
  return `/t/${thread.slug}/${thread.id}/`
}
export const threadLastPost = (thread: ISluggable) => {
  return `/t/${thread.slug}/${thread.id}/last/`
}
export const threadPost = (thread: ISluggable, post: { id: string }) => {
  return `/t/${thread.slug}/${thread.id}/post/${post.id}/`
}
export const user = (user: ISluggable) => `/u/${user.slug}/${user.id}/`
