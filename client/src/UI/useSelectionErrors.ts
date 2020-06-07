import React from "react"
import { IMutationError } from "../types"

const useSelectionErrors = <TSelectable extends { id: string }>(
  location: string,
  selection?: Array<TSelectable>,
  errors?: Array<IMutationError>
) => {
  const [state, setState] = React.useState<Record<string, IMutationError>>(
    () => {
      if (!selection || !errors) return {}
      return getSelectionErrors(location, selection, errors)
    }
  )

  const updated = React.useMemo(() => {
    if (!selection) return false
    return selection.length > Object.keys(state).length
  }, [selection, state])

  return {
    updated,
    errors: state,
    clearErrors: () => setState({}),
    setErrors: (
      selection: Array<TSelectable>,
      errors: Array<IMutationError>
    ) => {
      const newErrors = getSelectionErrors(location, selection, errors)
      setState(newErrors)
    },
  }
}

const getSelectionErrors = <TSelectable extends { id: string }>(
  location: string,
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

  return newErrors
}

export { getSelectionErrors, useSelectionErrors }
