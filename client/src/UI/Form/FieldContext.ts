import React from "react"

interface FieldContextData {
  disabled?: boolean
  id?: string
  invalid?: boolean
  name?: string
  required?: boolean
}

const FieldContext = React.createContext<FieldContextData>({})

const useFieldContext = () => React.useContext(FieldContext)

export { FieldContext, useFieldContext }
