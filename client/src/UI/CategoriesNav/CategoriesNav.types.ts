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
  category: { id: string }
  parent: { id: string }
}
