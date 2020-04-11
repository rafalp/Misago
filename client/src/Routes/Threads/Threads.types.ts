import { ICategory } from "../../types"

export interface IActiveCategory {
  category: ICategory
  parent: ICategory
}

export interface IThreadsProps {
  openCategoryPicker: (active?: IActiveCategory | null) => void
}
