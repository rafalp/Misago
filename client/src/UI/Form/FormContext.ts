import React from "react"

interface IFormContext {
  id?: string
  disabled?: boolean
}

const FormContext = React.createContext<IFormContext>({})

const useFormContext = () => React.useContext(FormContext)

export { FormContext, useFormContext }
