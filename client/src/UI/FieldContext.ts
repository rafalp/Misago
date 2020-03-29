import React from "react"

interface IFieldContext {
  disabled?: boolean
  id?: string
  invalid?: boolean
  name?: string
  required?: boolean
}

const FieldContext = React.createContext<IFieldContext>({})

export default FieldContext
