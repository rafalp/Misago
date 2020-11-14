import { t } from "@lingui/macro"
import { useLingui } from "@lingui/react"
import React from "react"
import { useCategoriesListContext } from "../../Context"
import Select from "../Select"

const CategorySelect = () => {
  const { i18n } = useLingui()
  const categories = useCategoriesListContext()

  return (
    <Select
      emptyLabel={i18n._(
        "select_category.placeholder",
        t`- select category -`
      )}
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
