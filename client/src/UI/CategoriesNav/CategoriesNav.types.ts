export interface ICategory {
  id: string
  name: string
  slug: string
  color: string
  children: Array<IChild>
}

export interface IChild {
  id: string
  name: string
  slug: string
  color: string
}

export interface IActiveCategory {
  id: string
  parent: { id: string } | null
}
