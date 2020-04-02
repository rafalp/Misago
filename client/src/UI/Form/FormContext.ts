import React from "react"

interface IFormContext {
  id?: string
  disabled?: boolean
}

const FormContext = React.createContext<IFormContext>({})

export default FormContext
