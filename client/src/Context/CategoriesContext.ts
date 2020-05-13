import React from "react"
import { ICategory } from "../types"

const CategoriesContext = React.createContext<Array<ICategory>>([])

const useCategoriesContext = () => React.useContext(CategoriesContext)

const useCategoriesListContext = () => {
  const categories = useCategoriesContext()
  return React.useMemo(() => {
    const choices: Array<{ category: ICategory; depth: number }> = []
    categories.forEach((category) => {
      choices.push({ category, depth: 0 })
      category.children.forEach((child) =>
        choices.push({ category: child, depth: 1 })
      )
    })
    return choices
  }, [categories])
}

export { CategoriesContext, useCategoriesContext, useCategoriesListContext }
