import { ICategory } from "../../types"

export interface IActiveCategory {
  category: ICategory
  parent: ICategory
}

export interface IThreadsProps {
  openCategoryPicker: (active?: IActiveCategory | null) => void
}

export interface IThread {
  id: string
  title: string
  slug: string
  category: IThreadCategory
}

export interface IThreadCategory {
  id: string
  name: string
  slug: string
  color: string | null
  icon: string | null
  parent: IThreadCategory | null
}