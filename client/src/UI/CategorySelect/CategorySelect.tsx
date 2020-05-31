import { t } from "@lingui/macro"
import { I18n } from "@lingui/react"
import React from "react"
import { useCategoriesListContext } from "../../Context"
import Select from "../Select"

const CategorySelect = () => {
  const categories = useCategoriesListContext()

  return (
    <I18n>
      {({ i18n }) => (
        <Select
          emptyLabel={i18n._(
            t("select_category.placeholder")`- select category -`
          )}
          emptyValue=""
          options={categories.map(({ category, parent }) => {
            return {
              value: category.id,
              name: parent
                ? parent.name + " \\ " + category.name
                : category.name,
            }
          })}
        />
      )}
    </I18n>
  )
}

export default CategorySelect
