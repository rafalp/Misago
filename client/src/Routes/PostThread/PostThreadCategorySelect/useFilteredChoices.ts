import React from "react"
import useSearchQuery from "../../../UI/useSearchQuery"
import { CategoryChoice } from "../PostThread.types"

const useFilteredChoices = (
  choices: Array<CategoryChoice>,
  search: string
) => {
  const query = useSearchQuery(search)

  return React.useMemo(() => {
    if (query.trim().length === 0) {
      return choices
    }

    const results = choices.map((category) => {
      const foundChildren = category.children.filter((child) => {
        return child.name.toLowerCase().indexOf(query) >= 0
      })

      if (
        category.name.toLowerCase().indexOf(query) >= 0 ||
        foundChildren.length
      ) {
        return Object.assign({}, category, { children: foundChildren })
      }

      return null
    })

    return results.filter((result) => {
      return result !== null
    }) as Array<CategoryChoice>
  }, [choices, query])
}

export default useFilteredChoices
