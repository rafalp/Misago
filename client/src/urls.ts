export const index = () => "/"

interface Sluggable {
  id: string
  slug: string
}

export const categories = () => `/categories/`
export const category = (category: Sluggable) => {
  return `/c/${category.slug}/${category.id}/`
}
export const startThread = (category?: Sluggable | null) => {
  if (category) return `/start-thread/${category.slug}/${category.id}/`
  return `/start-thread/`
}
export const threads = () => `/threads/`
export const thread = (thread: Sluggable) => `/t/${thread.slug}/${thread.id}/`
export const user = (user: Sluggable) => `/u/${user.slug}/${user.id}/`
