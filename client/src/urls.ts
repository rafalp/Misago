export const index = () => "/"

interface Sluggable {
  id: string | number
  slug: string
}

interface ThreadParams extends Sluggable {
  page?: number
}

export const categories = () => `/categories/`
export const category = (category: Sluggable) => {
  return `/c/${category.slug}/${category.id}/`
}
export const post = (post: { id: string | number }) => {
  return `/post/${post.id}/`
}
export const postThread = (category?: Sluggable | null) => {
  if (category) return `/c/${category.slug}/${category.id}/post-thread/`
  return `/post-thread/`
}
export const threads = () => `/threads/`
export const thread = (thread: ThreadParams) => {
  if (thread.page && thread.page > 1) {
    return `/t/${thread.slug}/${thread.id}/${thread.page}/`
  }
  return `/t/${thread.slug}/${thread.id}/`
}
export const threadLastPost = (thread: Sluggable) => {
  return `/t/${thread.slug}/${thread.id}/last/`
}
export const threadPost = (
  thread: Sluggable,
  post: { id: string | number }
) => {
  return `/t/${thread.slug}/${thread.id}/post/${post.id}/`
}
export const user = (user: Sluggable) => `/u/${user.slug}/${user.id}/`
