import React from "react"
import { CategoriesContext } from "../../Context"
import { IActiveCategory } from "./ThreadsList.types"

const useActiveCategory = (id?: string | null) => {
  const categories = React.useContext(CategoriesContext)
  const [category, setCategory] = React.useState<IActiveCategory | null>(null)

  React.useEffect(() => {
    if (!id) return

    categories.find((item) => {
      if (item.id === id) {
        setCategory({ category: item, parent: item })
        return true
      }

      item.children.find((child) => {
        if (child.id === id) {
          setCategory({ category: child, parent: item })
          return true
        }

        return false
      })

      return false
    })
  }, [id, categories])

  return category
}

export default useActiveCategory
