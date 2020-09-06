import React from "react"
import { ICategoryChoice, ICategoryChoiceChild } from "../PostThread.types"

const useCategoryChoice = (value: string, choices: Array<ICategoryChoice>) => {
  const parent = React.useMemo<ICategoryChoice | undefined>(() => {
    return choices.find((category) => {
      if (category.id === value) return true

      return category.children.find((child) => {
        return child.id === value
      })
    })
  }, [value, choices])

  const child = React.useMemo<ICategoryChoiceChild | undefined>(() => {
    if (!parent) return undefined

    return parent.children.find((category) => {
      if (category.id === value) return true
    })
  }, [choices, parent, value])

  return { parent, child }
}

export default useCategoryChoice
