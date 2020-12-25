import React from "react"
import { useCategoriesContext } from "../../Context"
import { ActiveCategory } from "./Threads.types"

const useActiveCategory = (id?: string | null) => {
  const categories = useCategoriesContext()

  return React.useMemo<ActiveCategory | null>(() => {
    if (!id) return null

    let category: ActiveCategory | null = null
    categories.find((item) => {
      if (item.id === id) {
        category = { category: item, parent: item }
        return true
      }

      item.children.find((child) => {
        if (child.id === id) {
          category = { category: child, parent: item }
          return true
        }

        return false
      })

      return false
    })

    return category
  }, [id, categories])
}

export default useActiveCategory
