import React from "react"
import { AuthUser } from "../../types"
import { CategoryChoice } from "./PostThread.types"

const useValidCategories = (
  user: AuthUser | null,
  choices: Array<CategoryChoice>
) => {
  const isModerator = user ? user.isModerator : false
  return React.useMemo(() => {
    const validCategories: Array<string> = []
    choices.forEach((choice) => {
      if (isModerator || !choice.isClosed) {
        validCategories.push(choice.id)
      }
      choice.children.forEach((child) => {
        if (isModerator || !child.isClosed) {
          validCategories.push(child.id)
        }
      })
    })
    return validCategories
  }, [isModerator, choices])
}

export default useValidCategories
