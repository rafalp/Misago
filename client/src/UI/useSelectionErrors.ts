import React from "react"
import { IMutationError } from "../types"

const useSelectionErrors = <TSelectable extends { id: string }>(
  location: string
) => {
  const [errors, setErrors] = React.useState<Record<string, IMutationError>>(
    {}
  )

  return {
    errors,
    clearErrors: () => setErrors({}),
    setErrors: (
      selection: Array<TSelectable>,
      errors: Array<IMutationError>
    ) => {
      const newErrors: Record<string, IMutationError> = {}
      const indexToId: Record<string, string> = {}

      selection.forEach((item, i) => {
        indexToId[String(i)] = item.id
      })

      errors.forEach((error) => {
        if (error.location[0] !== location) return
        if (!indexToId[error.location[1]]) return

        const id = indexToId[error.location[1]]
        if (!newErrors[id]) {
          newErrors[id] = error
        }
      })

      setErrors(newErrors)
    },
  }
}

export default useSelectionErrors
