import { t } from "@lingui/macro"
import React from "react"
import { useCategoriesListContext } from "../../Context"
import Select from "../Select"

const CategorySelect = () => {
  const categories = useCategoriesListContext()

  return (
    <Select
      emptyLabel={t({
        id: "select_category.placeholder",
        message: "- select category -",
      })}
      emptyValue=""
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
