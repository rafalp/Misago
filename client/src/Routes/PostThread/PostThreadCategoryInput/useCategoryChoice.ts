import React from "react"
import { CategoryChoice, CategoryChoiceChild } from "../PostThread.types"

const useCategoryChoice = (value: string, choices: Array<CategoryChoice>) => {
  const parent = React.useMemo<CategoryChoice | null>(() => {
    return (
      choices.find((category) => {
        if (category.id === value) return true

        return !!category.children.find((child) => {
          return child.id === value
        })
      }) || null
    )
  }, [value, choices])

  const child = React.useMemo<CategoryChoiceChild | null>(() => {
    if (!parent) return null

    return (
      parent.children.find((category) => {
        return category.id === value
      }) || null
    )
  }, [parent, value])

  return { parent, child }
}

export default useCategoryChoice
