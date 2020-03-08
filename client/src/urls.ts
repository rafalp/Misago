export const index = () => "/"

interface Sluggable {
  id: string
  slug: string
}

export const user = (user: Sluggable) => `/u/${user.slug}/${user.id}/`