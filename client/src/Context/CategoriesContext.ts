import React from "react"
import { Category } from "../types"

const CategoriesContext = React.createContext<Array<Category>>([])

const useCategoriesContext = () => React.useContext(CategoriesContext)

const useCategoriesListContext = () => {
  const categories = useCategoriesContext()
  return React.useMemo(() => {
    const choices: Array<{
      category: Category
      parent?: Category
      depth: number
    }> = []
    categories.forEach((category) => {
      choices.push({ category, depth: 0 })
      category.children.forEach((child) =>
        choices.push({ category: child, parent: category, depth: 1 })
      )
    })
    return choices
  }, [categories])
}

export { CategoriesContext, useCategoriesContext, useCategoriesListContext }
