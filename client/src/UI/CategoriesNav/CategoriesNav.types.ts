export interface Category {
  id: string
  name: string
  slug: string
  color: string | null
  icon: string | null
  children: Array<ChildCategory>
}

export interface ChildCategory {
  id: string
  name: string
  slug: string
  color: string | null
  icon: string | null
}

export interface ActiveCategory {
  category: { id: string }
  parent: { id: string }
}
