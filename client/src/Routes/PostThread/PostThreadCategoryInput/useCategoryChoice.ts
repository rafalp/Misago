import React from "react"
import { ICategoryChoice, ICategoryChoiceChild } from "../PostThread.types"

const useCategoryChoice = (value: string, choices: Array<ICategoryChoice>) => {
  const parent = React.useMemo<ICategoryChoice | null>(() => {
    return (
      choices.find((category) => {
        if (category.id === value) return true

        return !!category.children.find((child) => {
          return child.id === value
        })
      }) || null
    )
  }, [value, choices])

  const child = React.useMemo<ICategoryChoiceChild | null>(() => {
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
