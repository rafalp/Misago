import React from "react"
import { MutationError } from "../types"

const useLocationError = (
  location: string,
  errors?: Array<MutationError> | null
) => {
  return React.useMemo(() => {
    for (const error of errors || []) {
      const errorLocation = error.location.join(".")
      if (errorLocation === location) {
        return error
      }
    }
    return null
  }, [location, errors])
}

export default useLocationError
