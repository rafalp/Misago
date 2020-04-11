import { ICategory } from "../../types"

export interface IActiveCategory {
  category: ICategory
  parent: ICategory
}

export interface IThreadsListProps {
  openCategoryPicker: (active?: IActiveCategory | null) => void
}
