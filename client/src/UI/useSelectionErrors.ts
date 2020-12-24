import React from "react"
import { MutationError } from "../types"

const useSelectionErrors = <TSelectable extends { id: string }>(
  location: string,
  selection?: Array<TSelectable>,
  errors?: Array<MutationError>
) => {
  const [state, setState] = React.useState<Record<string, MutationError>>(
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
      errors: Array<MutationError>
    ) => {
      const newErrors = getSelectionErrors(location, selection, errors)
      setState(newErrors)
    },
  }
}

const getSelectionErrors = <TSelectable extends { id: string }>(
  location: string,
  selection: Array<TSelectable>,
  errors: Array<MutationError>
) => {
  const newErrors: Record<string, MutationError> = {}
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
