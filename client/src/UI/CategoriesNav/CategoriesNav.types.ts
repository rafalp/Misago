export interface ICategory {
  id: string
  name: string
  slug: string
  color: string | null
  icon: string | null
  children: Array<IChild>
}

export interface IChild {
  id: string
  name: string
  slug: string
  color: string | null
  icon: string | null
}

export interface IActiveCategory {
  id: string
  parent: { id: string } | null
}
