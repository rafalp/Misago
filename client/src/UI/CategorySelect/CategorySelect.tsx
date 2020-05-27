import React from "react"
import { useCategoriesListContext } from "../../Context"
import Select from "../Select"

const CategorySelect = () => {
  const categories = useCategoriesListContext()

  return (
    <Select
      options={categories.map(({ category, parent }) => {
        return {
          value: category.id,
          name: parent ? parent.name + " \\ " + category.name : category.name,
        }
      })}
    />
  )
}

export default CategorySelect
