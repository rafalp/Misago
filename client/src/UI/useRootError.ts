import React from "react"
import { MutationError } from "../types"

const useRootError = (errors?: Array<MutationError> | null) => {
  return React.useMemo(() => {
    for (const error of errors || []) {
      const errorLocation = error.location.join(".")
      if (errorLocation === "__root__") {
        return error
      }
    }
    return null
  }, [errors])
}

export default useRootError
