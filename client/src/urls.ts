export const index = () => "/"

interface Sluggable {
  id: string
  slug: string
}

export const categories = () => `/categories/`
export const category = (category: Sluggable) => {
  return `/c/${category.slug}/${category.id}/`
}
export const startThread = () => `/start-thread/`
export const thread = (thread: Sluggable) => `/t/${thread.slug}/${thread.id}/`
export const user = (user: Sluggable) => `/u/${user.slug}/${user.id}/`
